from ewis.core.engine import EWISEngine
from ewis.plugins.builtin.cooling_optimizer import CoolingOptimizerPlugin


def test_engine_runs_with_plugin():
    engine = EWISEngine()
    engine.register(CoolingOptimizerPlugin())
    payload = {
        "datacenter_id":"DC-1",
        "region":"TEST",
        "timestamp_utc":"2026-03-03T00:00:00Z",
        "power_mw": 10.0,
        "it_load_mw": 8.0,
        "pue": 1.2,
    }
    report = engine.run(payload)
    s = report.summary()
    assert s["datacenter_id"] == "DC-1"
    assert "grid_stress_index" in s["metrics"]
