"""Normalise FortyGuard result variants into Curo's public data shape."""

from typing import Any


def celsius_to_fahrenheit(value: float) -> float:
    """Convert Celsius to Fahrenheit."""

    return round((float(value) * 9 / 5) + 32, 1)


def _number(value: Any) -> float | None:
    """Read a finite numeric value from a permissive API field."""

    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if number == number else None


def temperature_celsius(properties: dict[str, Any]) -> float | None:
    """Find a temperature value in known GeoJSON property names."""

    for key in ("temperature_celsius", "temperature", "temp_c", "temp", "tcm", "value", "mean"):
        value = _number(properties.get(key))
        if value is not None:
            return value
    return None


def features(result: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract GeoJSON features from a completed response."""

    data = result.get("data", {})
    nested = data.get("result", data)
    map_data = nested.get("map_data", {}) if isinstance(nested, dict) else {}
    if isinstance(map_data, dict) and map_data.get("type") == "FeatureCollection":
        return [feature for feature in map_data.get("features", []) if isinstance(feature, dict)]
    if isinstance(map_data, list):
        return [feature for feature in map_data if isinstance(feature, dict)]
    return []


def stats_temperature_celsius(result: dict[str, Any]) -> float | None:
    """Extract an area mean temperature when the result supplies statistics."""

    data = result.get("data", {})
    nested = data.get("result", data)
    stats = nested.get("stats_data", {}) if isinstance(nested, dict) else {}
    temperature_stats = stats.get("Temperature_stats", stats.get("temperature_stats", {})) if isinstance(stats, dict) else {}
    if isinstance(temperature_stats, dict):
        for key in ("Mean", "mean", "Average", "average"):
            value = _number(temperature_stats.get(key))
            if value is not None:
                return value
    return None


def normalise_heatmap(result: dict[str, Any], timestamp: str, source: str) -> dict[str, Any]:
    """Return cells and an area temperature from a raw heatmap response."""

    output_cells = []
    values = []
    for index, feature in enumerate(features(result)):
        properties = feature.get("properties", {}) or {}
        temp_c = temperature_celsius(properties)
        geometry = feature.get("geometry", {}) or {}
        coordinates = geometry.get("coordinates", [])
        if temp_c is None:
            continue
        values.append(celsius_to_fahrenheit(temp_c))
        output_cells.append({"id": f"cell-{index}", "bounds": coordinates[0] if geometry.get("type") == "Polygon" and coordinates else coordinates, "tempF": celsius_to_fahrenheit(temp_c), "source": source})
    mean_c = stats_temperature_celsius(result)
    mean_f = celsius_to_fahrenheit(mean_c) if mean_c is not None else (round(sum(values) / len(values), 1) if values else None)
    return {"cells": output_cells, "meanTempF": mean_f, "minTempF": min(values) if values else None, "maxTempF": max(values) if values else None, "timestamp": timestamp, "source": source}

