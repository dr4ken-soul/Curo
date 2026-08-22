"""Verify current, forecast, and historical FortyGuard data for Phoenix."""

import asyncio
import sys
from datetime import datetime, timezone

from curo.cache import CacheStore
from curo.config import get_settings
from curo.fortyguard import FortyGuardClient, forecast_hours, hour_payload
from curo.normalise import normalise_heatmap


async def verify() -> int:
    """Run the three provider checks and return a process exit code."""

    settings = get_settings()
    cache = CacheStore(settings.curo_db_path)
    client = FortyGuardClient(settings, cache)
    if not client.configured:
        print("ERROR: FORTYGUARD_API_KEY is not configured", file=sys.stderr)
        return 1
    now = datetime.now(timezone.utc)
    checks = [("current", now), ("forecast", forecast_hours(now)[1]), ("history", datetime(max(2021, now.year - 1), now.month, now.day, 12, tzinfo=timezone.utc))]
    for label, timestamp in checks:
        try:
            response = await client.heatmap(hour_payload(33.4484, -112.0740, timestamp), label)
            data = normalise_heatmap(response["payload"], timestamp.isoformat(), response["source"])
            if data["meanTempF"] is None and not data["cells"]:
                raise RuntimeError("response contained no readable temperature")
            print(f"{label}: {data['meanTempF']} F · source {response['source']} · {data['timestamp']}")
        except Exception as error:  # noqa: BLE001
            print(f"ERROR {label}: {error}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(verify()))

