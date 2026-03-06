from phiak.core.engine import PHIAKEngine, EngineConfig
from phiak.plugins.builtin.small_cell_suppression import SmallCellSuppressionPlugin
from phiak.plugins.builtin.early_warning import EarlyWarningPlugin


def test_engine_runs_from_paths(tmp_path):
    inc = tmp_path/"inc.csv"
    cap = tmp_path/"cap.csv"
    ww = tmp_path/"ww.csv"

    inc.write_text("date,geo_id,geo_level,pathogen,cases,tests,positive\n2026-01-01,X,county,COVID,12,100,10\n")
    cap.write_text("date,geo_id,facility_type,ed_beds_total,ed_beds_available\n2026-01-01,X,hospital,10,2\n")
    ww.write_text("date,geo_id,site_id,target,gene_copies_ml,flow_m3_d,lab_qc_flag\n2026-01-01,X,S1,SARS-CoV-2,1000,10000,ok\n")

    engine = PHIAKEngine(EngineConfig(extra={}, suppression_k=11))
    engine.register(SmallCellSuppressionPlugin())
    engine.register(EarlyWarningPlugin())
    report = engine.run_from_paths(str(inc), str(cap), str(ww)).to_json_dict()
    assert report["inputs_summary"]["incidence_rows"] == 1
