import json, pathlib

def render_reports(run_dir, formats):
    run = pathlib.Path(run_dir)
    reports = run / "reports"
    reports.mkdir(parents=True, exist_ok=True)

    data = {}
    rpt_json = reports / "report.json"
    if rpt_json.exists():
        data = json.loads(rpt_json.read_text())
    else:
        data = {"project": "unknown", "findings": [], "metrics": {}, "run_id": "unknown"}

    if "md" in formats:
        md = []
        md.append(f"# Audit Report — {data.get('project','unknown')}")
        md.append(f"Run: {data.get('run_id','n/a')}")
        md.append("\n## Findings")
        if data.get("findings"):
            for f in data["findings"]:
                md.append(f"- **{f['id']}** [{f['severity']} / {f['category']}] — {f['description']}")
        else:
            md.append("- None")
        md.append("\n## Metrics")
        for k, v in (data.get("metrics") or {}).items():
            md.append(f"- {k}: {v}")
        (reports / "report.md").write_text("\n".join(md))

    if "json" in formats and rpt_json.exists():
        pass  # canonical already exists

    if "pdf" in formats:
        (reports / "report.pdf").write_bytes(b"%PDF-1.4\n% placeholder PDF\n")
