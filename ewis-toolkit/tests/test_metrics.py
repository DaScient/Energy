from ewis.metrics.core import grid_stress_index


def test_gsi_none_without_grid_fields():
    payload = {"power_mw": 10.0, "it_load_mw": 8.0, "pue": 1.2, "datacenter_id":"x","region":"y","timestamp_utc":"t"}
    out = grid_stress_index(payload)
    assert out["value"] is None


def test_gsi_value_with_grid_fields():
    payload = {
        "datacenter_id":"x","region":"y","timestamp_utc":"t",
        "power_mw": 10.0,
        "it_load_mw": 8.0,
        "pue": 1.2,
        "grid_capacity_mw": 100.0,
        "base_grid_load_mw": 80.0,
        "ambient_temp_c": 30.0,
        "humidity_pct": 50.0,
    }
    out = grid_stress_index(payload)
    assert out["value"] is not None
    assert out["value"] > 0
