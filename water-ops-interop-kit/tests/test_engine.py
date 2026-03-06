from woik.core.engine import WOIKEngine
from woik.plugins.builtin.leak_detector import LeakDetectorPlugin


def test_engine_runs():
    engine = WOIKEngine()
    engine.register(LeakDetectorPlugin())
    payload = {
        "system_id":"X",
        "asset_id":"A",
        "asset_type":"pump_station",
        "timestamp_utc":"2026-03-05T00:00:00Z",
        "flow_m3_s":0.4,
        "pressure_kpa":450,
        "level_m":1.0,
    }
    report = engine.run(payload)
    s = report.summary()
    assert s["asset_id"] == "A"
    assert "leak_likelihood_score" in s["metrics"]
