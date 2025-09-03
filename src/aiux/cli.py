import click
from .auditor import run_audit
from .reporting import render_reports

@click.group()
def main():
    """ai-ux-auditor CLI"""
    pass

@main.command()
@click.option("--dom", type=click.Path(exists=True), help="DOM snapshot JSON")
@click.option("--screenshots", type=click.Path(exists=True), help="Folder of screenshots")
@click.option("--surveys", type=click.Path(exists=True), help="CSV of survey responses")
@click.option("--transcripts", type=click.Path(exists=True), help="Folder of transcripts")
@click.option("--config", type=click.Path(exists=True), required=True, help="YAML config")
@click.option("--out", "out_dir", type=click.Path(), required=True, help="Output run dir")
def audit(dom, screenshots, surveys, transcripts, config, out_dir):
    """Run audit and produce canonical artifacts."""
    run_audit(dom, screenshots, surveys, transcripts, config, out_dir)
    click.echo(f"Audit complete → {out_dir}")

@main.command()
@click.option("--run", "run_dir", type=click.Path(exists=True), required=True, help="Run dir from `aiux audit`")
@click.option("--format", "formats", default="md", help="Comma-separated: json,csv,md,pdf")
def report(run_dir, formats):
    """Render human-readable reports from canonical artifacts."""
    fmts = [f.strip() for f in formats.split(",") if f.strip()]
    render_reports(run_dir, fmts)
    click.echo(f"Report(s) written → {run_dir}/reports")
