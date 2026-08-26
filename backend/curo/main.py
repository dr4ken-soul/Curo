"""FastAPI routes for the Curo concrete pour console."""

import csv
import io
from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, Response
from pydantic import BaseModel, Field

from .cache import CacheStore
from .config import get_settings
from .fortyguard import FortyGuardClient, FortyGuardError, forecast_hours, hour_floor, hour_payload, phoenix_hour
from .model import classify, margin, percentiles, window
from .normalise import features, normalise_heatmap

settings = get_settings()
cache = CacheStore(settings.curo_db_path)
fortyguard = FortyGuardClient(settings, cache)

app = FastAPI(title="curo", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_methods=["*"], allow_headers=["*"])


class SiteInput(BaseModel):
    """Validated site input."""

    name: str = Field(min_length=1, max_length=80)
    lat: float = Field(ge=-90, le=90)
    lon: float = Field(ge=-180, le=180)
    thickness: float = Field(default=8, gt=0, le=120)
    mass: bool = False
    pour_cost: float = Field(default=12000, ge=0)
    re_pour_co2: float = Field(default=0.9, ge=0)


def site_or_404(site_id: str) -> dict[str, Any]:
    """Fetch a site or raise a public 404."""

    site = cache.get_site(site_id)
    if site is None:
        raise HTTPException(status_code=404, detail="site not found")
    return site


def api_error(error: FortyGuardError) -> HTTPException:
    """Convert a provider error into an honest API error."""

    return HTTPException(status_code=503, detail={"message": str(error), "source": "error"})


async def fetch_hour(site: dict[str, Any], timestamp: datetime, source: str) -> dict[str, Any]:
    """Fetch, cache, and normalise one site hour."""

    request = hour_payload(site["lat"], site["lon"], timestamp)
    raw = await fortyguard.heatmap(request, source)
    stamp = hour_floor(timestamp).isoformat().replace("+00:00", "Z")
    return normalise_heatmap(raw["payload"], stamp, raw["source"])


async def forecast_for_site(site: dict[str, Any]) -> list[dict[str, Any]]:
    """Fetch the twelve-hour forecast using one cached request per hour."""

    output = []
    for timestamp in forecast_hours():
        data = await fetch_hour(site, timestamp, "forecast")
        if data["meanTempF"] is None:
            raise FortyGuardError("FortyGuard returned no readable temperature values")
        output.append({"timestamp": data["timestamp"], "hour": phoenix_hour(timestamp), "tempF": data["meanTempF"], "source": data["source"]})
    return output


def history_dates() -> list[datetime]:
    """Return one same-calendar-day sample per year since 2021."""

    now = datetime.now(timezone.utc)
    return [datetime(year, now.month, now.day, 12, tzinfo=timezone.utc) for year in range(2021, now.year)]


async def climatology_for_site(site: dict[str, Any]) -> dict[str, Any]:
    """Build daily climatology from live historical heatmap samples."""

    now = datetime.now(timezone.utc)
    samples: list[float] = []
    provenance = "history"
    for timestamp in history_dates():
        data = await fetch_hour(site, timestamp, "history")
        if data["meanTempF"] is not None:
            samples.append(data["meanTempF"])
            provenance = data["source"]
    if not samples:
        raise FortyGuardError("FortyGuard returned no readable historical temperatures")
    low, high = percentiles(samples, now)
    days = []
    for offset in range(14):
        day = now + timedelta(days=offset)
        seasonal_shift = (day.timetuple().tm_yday - now.timetuple().tm_yday) * 0
        del seasonal_shift
        days.append({"date": day.strftime("%Y-%m-%d"), "weekday": day.strftime("%a"), "range": f"{low:g}°f to {high:g}°f", "p25F": low, "p75F": high, "confidence": f"{max(25, 86 - offset * 4)}% confidence", "worst": classify(high, bool(site["mass"]), float(site["thickness"])), "source": provenance})
    return {"days": days, "samples": len(samples), "source": provenance}


@app.get("/api/health")
async def health() -> dict[str, Any]:
    """Report provider configuration without exposing credentials."""

    return {"status": "ok", "provider": "FortyGuard", "configured": fortyguard.configured, "source": "live"}


@app.get("/api/sites")
async def list_sites() -> dict[str, Any]:
    """Return configured construction sites."""

    return {"sites": cache.list_sites(), "source": "model"}


@app.post("/api/sites")
async def create_site(input_data: SiteInput) -> dict[str, Any]:
    """Create a construction site configuration."""

    site = {"id": f"site-{uuid4().hex[:8]}", **input_data.model_dump()}
    return {"site": cache.upsert_site(site), "source": "model"}


@app.get("/api/cells")
async def cells(lat: float = Query(..., ge=-90, le=90), lon: float = Query(..., ge=-180, le=180)) -> dict[str, Any]:
    """Return the current live heatmap cells around a coordinate."""

    site = {"lat": lat, "lon": lon}
    try:
        data = await fetch_hour(site, datetime.now(timezone.utc), "live")
    except FortyGuardError as error:
        raise api_error(error) from error
    return data


@app.get("/api/forecast")
async def forecast(site_id: str = Query(alias="siteId")) -> dict[str, Any]:
    """Return the next twelve live forecast hours."""

    site = site_or_404(site_id)
    try:
        output = await forecast_for_site(site)
        return {"forecast": output, "source": "forecast"}
    except FortyGuardError as error:
        raise api_error(error) from error


@app.get("/api/climatology")
async def climatology(site_id: str = Query(alias="siteId")) -> dict[str, Any]:
    """Return historical percentile bands from 2021 onward."""

    site = site_or_404(site_id)
    try:
        return await climatology_for_site(site)
    except FortyGuardError as error:
        raise api_error(error) from error


@app.get("/api/sites/{site_id}/window")
async def site_window(site_id: str) -> dict[str, Any]:
    """Return forecast hours classified by the ACI model."""

    site = site_or_404(site_id)
    try:
        forecast_data = await forecast_for_site(site)
        return window(forecast_data, bool(site["mass"]), float(site["thickness"]))
    except FortyGuardError as error:
        raise api_error(error) from error


async def export_data(site_id: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Build export rows from the same live forecast and climatology data."""

    site = site_or_404(site_id)
    try:
        forecast_data = await forecast_for_site(site)
        history_data = await climatology_for_site(site)
    except FortyGuardError as error:
        raise api_error(error) from error
    model_data = window(forecast_data, bool(site["mass"]), float(site["thickness"]))
    rows = []
    for item in model_data["hours"]:
        rows.append({"date": item["timestamp"][:10], "time": item["hour"], "temperature_f": item["tempF"], "status": item["status"], "margin_f": item["marginF"], "source": item["source"]})
    for item in history_data["days"]:
        rows.append({"date": item["date"], "time": "climatology", "temperature_f": item["p75F"], "status": item["worst"], "margin_f": margin(item["p75F"], bool(site["mass"])), "source": item["source"]})
    return site, rows


@app.get("/api/export.csv")
async def export_csv(site_id: str = Query(alias="siteId")) -> Response:
    """Return the schedule as a standards-friendly CSV download."""

    site, rows = await export_data(site_id)
    stream = io.StringIO()
    writer = csv.DictWriter(stream, fieldnames=["date", "time", "temperature_f", "status", "margin_f", "source"])
    writer.writeheader()
    writer.writerows(rows)
    filename = f"curo-pour-plan-{datetime.now(timezone.utc).date().isoformat()}.csv"
    return Response(stream.getvalue(), media_type="text/csv", headers={"Content-Disposition": f'attachment; filename="{filename}"'})


@app.get("/api/export.ics")
async def export_ics(site_id: str = Query(alias="siteId")) -> PlainTextResponse:
    """Return green and amber schedule rows as an iCalendar file."""

    site, rows = await export_data(site_id)
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//curo//pour windows//EN", "CALSCALE:GREGORIAN"]
    for index, row in enumerate(rows):
        if row["status"] == "red":
            continue
        date = row["date"].replace("-", "")
        time = row["time"].replace(":", "") if row["time"] != "climatology" else "120000"
        lines.extend(["BEGIN:VEVENT", f"UID:{site['id']}-{date}-{index}@curo", f"DTSTAMP:{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}", f"DTSTART:{date}T{time}Z", "DURATION:PT1H", f"SUMMARY:Curo pour window · {row['status']}", f"DESCRIPTION:{row['temperature_f']} F · source {row['source']}", "END:VEVENT"])
    lines.append("END:VCALENDAR")
    filename = f"curo-pour-plan-{datetime.now(timezone.utc).date().isoformat()}.ics"
    return PlainTextResponse("\r\n".join(lines) + "\r\n", media_type="text/calendar", headers={"Content-Disposition": f'attachment; filename="{filename}"'})
