# ai-ux-auditor

AI-assisted accessibility and usability audit toolkit for **high-stakes systems** (healthcare, cybersecurity/privacy tools, DePIN operator dashboards).
Outputs **reproducible** findings mapped to **standards**, with artifacts suitable for engineering, compliance, and research review.

---

## What it does

* **Accessibility checks (WCAG 2.2 AA)** over DOM snapshots & screenshots (OCR-assisted).
* **Usability metrics**: task time, error rate, completion, SUS/NASA-TLX capture & aggregation.
* **Security-critical flow analysis**: auth, MFA, consent, key management, recovery, irreversible actions.
* **Heuristic evaluation** (Nielsen, cognitive walkthrough) with explainable rationales.
* **AI clustering** of qualitative data (survey free-text, transcripts, logs) → themes, exemplars, contradictions.
* **Standards mapping**: WCAG 2.2, ISO 9241-210, IEC 62366-1, NIST SP 800-53/63, GDPR Art. 5/25, LINDDUN/STRIDE, **SOC 2 TSC**.
* **Reports**: JSON (canonical schema), CSV (metrics), Markdown/PDF (human-readable), baseline diff.

---

## Use cases

* **Healthcare**: patient intake, clinician dashboards, surgical coordination; safety-critical confirmations.
* **Cybersecurity/Privacy**: key handling, MFA, consent, auditability, policy enforcement, breach UX drills.
* **DePIN**: operator/staker dashboards, resource scheduling, reliability/reward visibility, failure-mode comms.

---

## Architecture

ai-ux-auditor/
├─ **cli/** — command entry points (Python)
├─ **adapters/** — inputs (DOM, screenshots, logs, surveys, transcripts)
├─ **checks/** — accessibility, flows, heuristics, security-UX, domain packs
├─ **analyzers/** — clustering, scoring, standards mapping
├─ **reports/** — renderers (json, csv, md, pdf)
├─ **schemas/** — JSON Schemas for inputs/outputs
├─ **examples/** — sample inputs & expected outputs
└─ **docs/** — methods, references, standards crosswalk

* **Adapters** normalize inputs.
* **Checks** emit findings with `severity`, `evidence`, `standard_refs`.
* **Analyzers** aggregate and score.
* **Reporters** serialize to reproducible artifacts.

---

## Installation

```bash
# Python 3.10+ recommended
python -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -e .
```

*(Optional) PDF export requires wkhtmltopdf or Chrome/Chromium.*

---

## Quick start

```bash
# 1) Audit a DOM snapshot (JSON) + screenshots folder + optional research data
aiux audit \
  --dom ./examples/dom_snapshot.json \
  --screenshots ./examples/screens/ \
  --surveys ./examples/surveys.csv \
  --transcripts ./examples/transcripts/ \
  --config ./examples/config.yaml \
  --out ./run_001

# 2) Render human-readable report(s)
aiux report --run ./run_001 --format md,pdf
```

Outputs in `./run_001/reports/`:

* `report.json` (canonical)
* `metrics.csv`
* `report.md` / `report.pdf`
* `diff.json` (if a `--baseline` was provided)

---

## Input types

* **DOM snapshot**: serialized accessibility tree / computed styles (JSON).
* **Screenshots**: PNG/JPEG; OCR used for text extraction and contrast analysis.
* **Interaction logs**: JSONL with `timestamp`, `user_id`, `event`, `target`, `result`.
* **Surveys**: CSV (`respondent_id`, `q_id`, `scale`, `response`, `free_text`).
* **Transcripts**: text files per session; diarization optional.

Example survey row:

```
respondent_id,q_id,scale,response,free_text
u-001,SUS01,5,Strongly Agree,"Navigation was predictable"
```

---

## Configuration (YAML)

```yaml
project: "Clinician Dashboard v0.4"
domains: [healthcare, security]
checks:
  wcag:
    level: "AA"
    include: ["1.4.3", "2.4.7", "3.3.1"]
  flows:
    require_confirm_on_irreversible: true
    show_recovery_paths: true
  heuristics:
    enable_cognitive_walkthrough: true
  security_ux:
    mfa_visibility: required
    consent_logging: required
  clustering:
    model: "open-source-embed-xx"
    min_cluster_size: 5
report:
  formats: ["json","csv","md","pdf"]
  include_screenshots: true
baseline:
  path: "./run_000/report.json"   # optional
privacy:
  pii_scrub: true
  pii_fields: ["user_id","email","mrn"]
standards:
  soc2:
    enabled: true
    caps:
      common_criteria: ["CC6","CC7","CC8","CC9"]
      availability: ["A1"]
      confidentiality: ["C1"]
      processing_integrity: ["PI1"]
      privacy: ["P"]
```

---

## SOC 2 integration (Trust Services Criteria)

**Purpose.** Map UX/accessibility/security findings to **AICPA SOC 2 TSC (2017, rev. 2018)** and emit **auditor-consumable evidence**. Coverage includes **Common Criteria CC1–CC9** plus **A1 (Availability)**, **C1 (Confidentiality)**, **PI1 (Processing Integrity)**, **P (Privacy)**.

**Evidence artifacts (auto-generated):**

* `reports/soc2-matrix.csv` — finding → **TSC criterion** mapping (id, severity, owner, evidence link)
* `reports/soc2-matrix.md` — human-readable control matrix
* `reports/evidence/...` — screenshots, DOM excerpts, log snippets
* `reports/provenance.json` — run metadata (versions, seeds, config)

**Example mappings**

| Finding (example)                                          | TSC Ref      | How surfaced in UX                                 |
| ---------------------------------------------------------- | ------------ | -------------------------------------------------- |
| MFA required + recovery visible                            | CC6.1        | Auth UI requires MFA; recovery path explicit       |
| Session idle timeout with pre-expiry warning               | CC6.6        | Idle timer + warning banner; forced re-auth        |
| Consent events logged (immutable/exportable)               | CC7.2, P     | Consent confirmations logged w/ timestamps         |
| Pre-deployment change notice visible to operators          | CC8.x        | “What’s changing” banner + rollback link           |
| Role-based UI; admin functions segregated                  | CC6.3, CC6.7 | Restricted controls hidden/disabled for non-admins |
| Data classification indicators in UI                       | C1           | Field-level labels; export dialogs warn on scope   |
| Input validation + reconciliation for irreversible actions | PI1          | Validation, confirmation, consequence statement    |

**CSV columns (for auditors):**

```
finding_id, title, severity, tsc_refs, control_owner, evidence_path, remediation, status
```

---

## Mapping to standards (examples)

| Category       | Rule/Principle               | How we test / capture                                |
| -------------- | ---------------------------- | ---------------------------------------------------- |
| WCAG 2.2 AA    | 1.4.3 Contrast (Minimum)     | OCR text + contrast calc on screenshot regions       |
| WCAG 2.2 AA    | 2.4.7 Focus Visible          | DOM focus outline & tab order check                  |
| ISO 9241-210   | Human-centred design         | Study templates, task analyses, iterative logs       |
| IEC 62366-1    | Use error / risk controls    | Safety-critical confirmations; irreversible actions  |
| NIST SP 800-63 | Authenticator usability      | MFA discoverability, fallback, recovery flows        |
| NIST SP 800-53 | AU-2 / AR-8 auditing/consent | Consent log presence & transparency checks           |
| GDPR Art. 5/25 | Minimization / PbD           | Field exposure; consent & visibility in UI           |
| LINDDUN        | Privacy threats              | Checklist + UX evidence (where mitigations appear)   |
| STRIDE         | Threat modeling cues         | Error & recovery messaging; authority & confirmation |
| SOC 2 TSC      | CC6/7/8/9; A1; C1; PI1; P    | SOC 2 matrix output + evidence links                 |

---

## Metrics

* **SUS** (0–100), **NASA-TLX** (six subscales)
* **Completion rate**, **Time-on-task**, **Error rate**
* **Undo/Recovery presence**, **Irreversible action safeguards**
* **Adoption**: **TTFI (time-to-first-insight)**; setup time; required prerequisites

---

## Extending (custom check example)

```python
# /checks/check_irreversible.py
def run(dom, screenshots, config):
    findings = []
    for btn in dom.get('buttons', []):
        if btn.get('label') in ['Delete','Purge','Revoke'] and not btn.get('confirm'):
            findings.append({
                "id": f"IRREV-{btn['id']}",
                "category": "flow",
                "severity": "critical",
                "description": "Irreversible action without explicit confirmation",
                "locations": [btn['selector']],
                "standard_refs": ["IEC 62366-1","ISO 9241-210","CC9.2","PI1"],
                "remediation": "Add confirm with consequence statement and recovery path"
            })
    return findings
```

Register in `/checks/__init__.py` and enable via `config.yaml`.

---

## Reproducibility

* **Lockfiles**: `requirements.txt` (and `package-lock.json` if applicable)
* **Container**:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -U pip && pip install -e .
ENTRYPOINT ["aiux"]
```

* Deterministic seeds for clustering; versioned models.
* **Data**: sanitized or synthetic; no PHI/PII.

---

## Privacy & ethics

* No PHI/PII in repo or outputs.
* Built-in PII scrubbing (`privacy.pii_scrub: true`).
* Provenance and limitations emitted with each run.

---

## Roadmap

* DOM harvester (Playwright adapter).
* Screenshot OCR & region linking to DOM nodes.
* PDF/print artifact renderer with evidence panels.
* Healthcare pack: medication, orders, surgical stage confirmations.
* Security pack: keys, MFA recovery, device loss, consent diffs.
* DePIN pack: outage comms, reward variance, scheduling explainers.
* Baseline diffs + trend charts across releases.
* CI integration (fail on critical regressions).

---

## Contributing

* Open an issue with **task, metric, and standard mapping**.
* Include **before/after evidence** for UX changes.
* No sensitive data; use synthetic fixtures.

---

## Citation

If you reference outputs in papers/reports, cite the repo and tag a release (consider enabling Zenodo for a DOI).

---

## License

* **Code:** MIT
* **Docs/Data:** CC BY 4.0
  (Adjust in `LICENSE` and `/docs/LICENSE.md` per your policy.)

---

### References

WCAG 2.2; ISO 9241-210; IEC 62366-1; NIST SP 800-53/63; GDPR Art. 5/25; LINDDUN; STRIDE; **AICPA SOC 2 TSC (2017, rev. 2018)**.
