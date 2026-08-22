"""Deterministic ACI 305R-20 placement-window rules."""

from collections.abc import Iterable
from datetime import datetime
from statistics import quantiles
from typing import Any

PLACEMENT_LIMIT_F = 95.0
AMBER_BAND_F = 5.0


def effective_limit(mass: bool) -> float:
    """Return the placement limit after the mass-concrete adjustment."""

    return PLACEMENT_LIMIT_F - 10.0 if mass else PLACEMENT_LIMIT_F


def effective_amber_band(thickness: float) -> float:
    """Return the amber band after the slab-thickness adjustment."""

    return 7.0 if thickness > 12.0 else AMBER_BAND_F


def classify(temp_f: float, mass: bool = False, thickness: float = 8.0) -> str:
    """Classify a temperature as green, amber, or red."""

    limit = effective_limit(mass)
    band = effective_amber_band(thickness)
    if temp_f > limit:
        return "red"
    if temp_f >= limit - band:
        return "amber"
    return "green"


def margin(temp_f: float, mass: bool = False) -> float:
    """Return the signed degrees below the applicable placement limit."""

    return round(effective_limit(mass) - temp_f, 1)


def percentiles(history: Iterable[float], date: datetime | None = None) -> tuple[float, float]:
    """Return p25 and p75 for history, with a stable small-sample fallback."""

    del date
    values = sorted(float(value) for value in history)
    if not values:
        raise ValueError("history is empty")
    if len(values) == 1:
        return values[0], values[0]
    if len(values) == 2:
        return values[0], values[1]
    quartiles = quantiles(values, n=4, method="inclusive")
    return round(quartiles[0], 1), round(quartiles[2], 1)


def window(forecast: list[dict[str, Any]], mass: bool = False, thickness: float = 8.0) -> dict[str, Any]:
    """Classify every forecast hour and return the model explanation."""

    limit = effective_limit(mass)
    band = effective_amber_band(thickness)
    hours = []
    for item in forecast:
        temp_f = float(item["tempF"])
        status = classify(temp_f, mass, thickness)
        rules = [f"placement limit {limit:g}°f · aci 305r-20"]
        if mass:
            rules.append("mass concrete · limit tightened by 10°f")
        if thickness > 12:
            rules.append("slab thickness over 12in · amber band widened to 7°f")
        hours.append({**item, "status": status, "marginF": margin(temp_f, mass), "rules": rules})
    worst = "green"
    for status in ("red", "amber", "green"):
        if any(hour["status"] == status for hour in hours):
            worst = status
            break
    return {"hours": hours, "worst": worst, "limitF": limit, "amberBandF": band, "source": "model"}

