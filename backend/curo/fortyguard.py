"""Async client for FortyGuard's current asynchronous heatmap API."""

import asyncio
from datetime import datetime, timedelta, timezone
from typing import Any

import httpx

from .cache import CacheStore
from .config import Settings


class FortyGuardError(RuntimeError):
    """Raised when a FortyGuard request cannot be completed."""


class FortyGuardClient:
    """Submit and cache FortyGuard heatmap jobs."""

    def __init__(self, settings: Settings, cache: CacheStore) -> None:
        """Create a client using application settings and the shared cache."""

        self.settings = settings
        self.cache = cache

    @property
    def configured(self) -> bool:
        """Return whether a FortyGuard key is available."""

        return bool(self.settings.fortyguard_api_key)

    async def heatmap(self, payload: dict[str, Any], source: str) -> dict[str, Any]:
        """Return a completed heatmap result, using the cache before the network."""

        key = self.cache.key_for("fortyguard-heatmap", payload)
        cached = self.cache.get(key)
        if cached is not None:
            response, fetched_at = cached
            if self._has_temperature_output(response):
                return {"payload": response, "source": "cached", "fetchedAt": fetched_at, "requestedSource": source}
            self.cache.delete(key)
        if not self.configured:
            raise FortyGuardError("FORTYGUARD_API_KEY is not configured")

        headers = {"api-key": self.settings.fortyguard_api_key or "", "Content-Type": "application/json"}
        async with httpx.AsyncClient(base_url=self.settings.fortyguard_base_url, timeout=45) as client:
            try:
                submission = await client.post("/heatmap", headers=headers, json=payload)
                submission.raise_for_status()
                body = submission.json()
                activity_id = body.get("data", {}).get("activity_id")
                if not activity_id:
                    raise FortyGuardError("FortyGuard returned no activity_id")
                completed = await self._poll(client, headers, activity_id)
            except httpx.HTTPStatusError as error:
                detail = error.response.text[:300]
                raise FortyGuardError(f"FortyGuard returned {error.response.status_code}: {detail}") from error
            except httpx.HTTPError as error:
                raise FortyGuardError(f"FortyGuard network error: {error}") from error
        if self._has_temperature_output(completed):
            self.cache.set(key, completed)
        return {"payload": completed, "source": source, "fetchedAt": int(datetime.now(timezone.utc).timestamp()), "requestedSource": source}

    @staticmethod
    def _has_temperature_output(response: dict[str, Any]) -> bool:
        """Return whether a completed response contains usable heat data."""

        data = response.get("data", {})
        result = data.get("result", data) if isinstance(data, dict) else {}
        if not isinstance(result, dict):
            return False
        map_data = result.get("map_data", {})
        if isinstance(map_data, dict) and map_data.get("features"):
            return True
        stats = result.get("stats_data", {})
        if not isinstance(stats, dict):
            return False
        temperature_stats = stats.get("temperature_stats", stats.get("Temperature_stats", {}))
        return isinstance(temperature_stats, dict) and any(key in temperature_stats for key in ("mean", "Mean", "minimum", "Minimum", "maximum", "Maximum"))

    async def _poll(self, client: httpx.AsyncClient, headers: dict[str, str], activity_id: str) -> dict[str, Any]:
        """Poll one activity until it completes or fails."""

        for attempt in range(self.settings.curo_poll_attempts):
            response = await client.get(f"/status/{activity_id}", headers=headers)
            response.raise_for_status()
            body = response.json()
            status = str(body.get("data", {}).get("status", "")).lower()
            if status in {"completed", "succeeded", "success"}:
                return body
            if status in {"failed", "error"}:
                raise FortyGuardError(f"FortyGuard activity {activity_id} failed")
            if attempt < self.settings.curo_poll_attempts - 1:
                await asyncio.sleep(self.settings.curo_poll_seconds)
        raise FortyGuardError(f"FortyGuard activity {activity_id} timed out")


def hour_floor(value: datetime) -> datetime:
    """Round a datetime down to the start of its hour in UTC."""

    return value.astimezone(timezone.utc).replace(minute=0, second=0, microsecond=0)


def hour_payload(lat: float, lon: float, value: datetime, half_size: float = 0.012) -> dict[str, Any]:
    """Build a documented single-hour heatmap request around a point."""

    timestamp = hour_floor(value)
    polygon = [
        [lon - half_size, lat - half_size],
        [lon + half_size, lat - half_size],
        [lon + half_size, lat + half_size],
        [lon - half_size, lat + half_size],
        [lon - half_size, lat - half_size],
    ]
    return {
        "polygon_aoi": {"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "coordinates": [polygon]}}]},
        "date_time": {"start_date": timestamp.strftime("%Y-%m-%d"), "start_time": timestamp.strftime("%H:%M"), "filter_type": 1},
        "granularity": 100,
    }


def forecast_hours(now: datetime | None = None) -> list[datetime]:
    """Return the next twelve UTC hours accepted by the API."""

    start = hour_floor(now or datetime.now(timezone.utc))
    return [start + timedelta(hours=index) for index in range(12)]
