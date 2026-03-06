from woik.metrics.core import leak_likelihood_heuristic, pump_specific_energy, water_quality_risk


def test_leak_score_basic():
    payload = {"flow_m3_s": 0.5, "pressure_kpa": 420}
    out = leak_likelihood_heuristic(payload)
    assert out["value"] is not None


def test_pse_none_without_power():
    payload = {"flow_m3_s": 0.5}
    out = pump_specific_energy(payload)
    assert out["value"] is None


def test_wqri_none_when_empty():
    payload = {}
    out = water_quality_risk(payload)
    assert out["value"] is None
