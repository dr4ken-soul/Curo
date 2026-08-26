from datetime import datetime, timezone

from curo.model import classify, margin, percentiles, window
from curo.fortyguard import hour_payload
from curo.normalise import normalise_heatmap


def test_classify_uses_aci_limit_and_amber_band() -> None:
    assert classify(89) == "green"
    assert classify(90) == "amber"
    assert classify(95) == "amber"
    assert classify(95.1) == "red"


def test_mass_concrete_tightens_limit() -> None:
    assert classify(85, mass=True) == "amber"
    assert classify(86, mass=True) == "red"


def test_thick_slab_widens_amber_band() -> None:
    assert classify(88, thickness=13) == "amber"


def test_percentiles_and_window() -> None:
    assert percentiles([80, 90, 100], datetime(2026, 8, 22)) == (85.0, 95.0)
    result = window([{"timestamp": "2026-08-22T15:00:00Z", "hour": "15:00", "tempF": 102, "source": "forecast"}])
    assert result["worst"] == "red"
    assert result["hours"][0]["marginF"] == -7.0


def test_heatmap_request_uses_phoenix_local_time() -> None:
    payload = hour_payload(33.4484, -112.0740, datetime(2026, 8, 23, 12, tzinfo=timezone.utc))
    assert payload["date_time"]["start_date"] == "2026-08-23"
    assert payload["date_time"]["start_time"] == "05:00"


def test_normalise_reads_fortyguard_average_temperature_cells() -> None:
    result = normalise_heatmap(
        {
            "data": {
                "result": {
                    "map_data": {
                        "type": "FeatureCollection",
                        "features": [
                            {
                                "type": "Feature",
                                "properties": {"average_temperature": 33.86},
                                "geometry": {"type": "Polygon", "coordinates": [[[1, 2], [3, 2], [3, 4], [1, 2]]]}
                            }
                        ]
                    }
                }
            }
        },
        "2026-08-26T10:00:00Z",
        "live",
    )
    assert len(result["cells"]) == 1
    assert result["cells"][0]["tempF"] == 92.9
