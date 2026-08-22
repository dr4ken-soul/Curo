from datetime import datetime

from curo.model import classify, margin, percentiles, window


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

