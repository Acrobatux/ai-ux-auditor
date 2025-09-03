import csv, json, pathlib, time
from datetime import datetime

def run_audit(dom_path, screenshots_dir, surveys_csv, transcripts_dir, config_path, out_dir):
    out = pathlib.Path(out_dir)
    (out / "reports").mkdir(parents=True, exist_ok=True)
    (out / "evidence").mkdir(parents=True, exist_ok=True)

    report = {
        "project": pathlib.Path(config_path).stem,
        "run_id": f"run-{int(time.time())}",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "inputs": {
            "dom": str(dom_path) if dom_path else None,
            "screenshots": [],
            "surveys": str(surveys_csv) if surveys_csv else None,
            "transcripts": []
        },
        "findings": [
            {
                "id": "DEMO-001",
                "category": "wcag",
                "severity": "minor",
                "description": "Demo finding: placeholder contrast check",
                "evidence": "",
                "locations": [],
                "standard_refs": ["WCAG 2.2 1.4.3"],
                "remediation": "Run real checks once implemented."
            }
        ],
        "metrics": {
            "sus": None,
            "nasa_tlx": None,
            "time_on_task_ms": None,
            "completion_rate": None,
            "error_rate": None
        },
        "clusters": []
    }

    (out / "reports" / "report.json").write_text(json.dumps(report, indent=2))

    with (out / "reports" / "metrics.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["metric", "value"])
        w.writerow(["sus", ""])
        w.writerow(["time_on_task_ms", ""])
        w.writerow(["completion_rate", ""])
        w.writerow(["error_rate", ""])

    (out / "reports" / "provenance.json").write_text(
        json.dumps({"config": str(config_path), "version": "0.0.1"}, indent=2)
    )
