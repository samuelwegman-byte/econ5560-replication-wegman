# ECON 5560: Individual replication repository

GitHub account: **samuelwegman-byte**. This is Sam Wegman's individual version-control submission using Team 3's existing ECON 5560 replication project.

Repository: https://github.com/samuelwegman-byte/econ5560-replication-wegman

## Paper replicated

Eppink, Florian V., Matthew Winden, Will C. C. Wright, and Suzie Greenhalgh. 2016. "Non-Market Values in a Cost-Benefit World: Evidence from a Choice Experiment." *PLOS ONE* 11(10): e0165365. https://doi.org/10.1371/journal.pone.0165365

The paper studies whether attaching monetary information to development and environmental attributes changes how New Zealand councillors and council staff choose among hypothetical development projects. This repository packages Team 3's Python replication from the unchanged public Stata data through sample construction, descriptive statistics, conditional logit, mixed logit and sensitivity analysis, figures, tables, and discrepancy checks.

## Data source

The raw data are the authors' public **S1 Table: Choice experiment responses**. Original PLOS supplementary-data URL:

https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0165365.s001&type=supplementary

For this individual repository the file is retrieved during the fresh-checkout verification on **November 8, 2026** and then committed unchanged at `data/raw/S1Table.DTA`. The pipeline verifies SHA-256:

`ea292824db6b36ef18961aa954f0cb7964af5a7285d7e479840cf7aef19f3df2`

See `DATA_SOURCE.md` for provenance and attribution.

## How to run from a fresh clone

Use Python 3.12. After cloning, the final repository contains the raw data, so no internet connection is needed after the Python packages have been installed.

### macOS / Linux

```bash
git clone https://github.com/samuelwegman-byte/econ5560-replication-wegman.git
cd econ5560-replication-wegman
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
rm -rf outputs
mkdir -p logs
python run_all.py > logs/run_log.txt 2>&1
python -m pip freeze > logs/requirements.txt
```

### Windows PowerShell

```powershell
git clone https://github.com/samuelwegman-byte/econ5560-replication-wegman.git
cd econ5560-replication-wegman
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Remove-Item -Recurse -Force outputs -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force logs
python run_all.py *> logs\run_log.txt
python -m pip freeze > logs\requirements.txt
```

The master script executes all eight numbered Python stages in order and stops if any stage fails. It validates the raw checksum, analytical sample sizes, choice-set consistency, numerical table outputs, published-exhibit reproductions, dashboard generation, and mixed-logit convergence. Each stage runs in a fresh subprocess.

## Software and packages

The required direct Python dependencies are pinned in `requirements.txt`:

- Python 3.12
- NumPy 1.26.4
- pandas 2.3.3
- SciPy 1.13.1
- statsmodels 0.14.6
- Matplotlib 3.9.4

The exact environment used for the independent fresh-checkout verification is recorded in `logs/requirements.txt` and the final 20 lines of `logs/run_log.txt`.

## Runtime

The independently verified full run took **636.26 seconds (10 minutes 36 seconds)** on a GitHub-hosted Linux runner using Python **3.12.16**. The run regenerated **39 output files**, and both primary mixed-logit models converged. The same measured results are recorded in `logs/run_summary.json` and `logs/FRESH_CLONE.md`.

## Files

- `run_all.py` — master script; runs the entire replication, validates outputs, records timing and environment information.
- `requirements.txt` — pinned direct Python dependencies.
- `requirements-notebook.txt` — optional Jupyter dependencies; not required for the pipeline.
- `README.md` — reproduction instructions and limitations.
- `DATA_SOURCE.md` — raw-data source, retrieval date, checksum, and license.
- `SOURCE_PROVENANCE.md` — team-code attribution and individual packaging changes.
- `FILES.md` — one-line inventory of committed project files.
- `data/raw/S1Table.DTA` — unchanged author-provided raw data.
- `scripts/common.py` — shared paths, published comparison values, and model estimators.
- `scripts/01_parse_data.py` — parses raw data, reconstructs samples, and creates analysis variables.
- `scripts/02_descriptives.py` — creates respondent descriptives, card counts, and treatment choice rates.
- `scripts/03_conditional_logit.py` — estimates conditional-logit specifications.
- `scripts/04_mixed_logit.py` — estimates mixed-logit models and simulation sensitivity.
- `scripts/05_build_dashboard.py` — creates the offline dashboard.
- `scripts/06_slide_figures.py` — creates presentation figures.
- `scripts/07_paper_figures.py` — recreates the paper exhibits and comparison files.
- `scripts/08_debug_discrepancies.py` — diagnoses mismatches with published cells.
- `scripts/crosscheck_clogit.R` — optional independent R conditional-logit check.
- `scripts/replication_walkthrough.ipynb` — optional narrated walkthrough; not required by `run_all.py`.
- `scripts/REPLICATION_LOG.md` — historical Team 3 replication notes and hypotheses.
- `scripts/dashboard/template.html` — source template for the generated dashboard.
- `scripts/replication-targets/` — published exhibit reference images used for visual comparisons.
- `outputs/` — regenerated data, tables, figures, results, dashboard, and presentation/paper exhibits.
- `logs/run_log.txt` — stdout/stderr from the complete clean verification run.
- `logs/run_summary.json` — runtime, environment, validation, and convergence summary.
- `logs/requirements.txt` — exact `pip freeze` from the verification environment.
- `logs/output_sha256.txt` — checksums for regenerated outputs.
- `.github/workflows/verify-replication.yml` — fresh-checkout verification used for this individual submission.

See `FILES.md` for the complete generated-file inventory.

## What did not reproduce exactly

A successful run means the package executes from raw data and regenerates the committed outputs; it does **not** mean every published number matches exactly.

The Team 3 reconstruction reproduces the reported analytical sample sizes and many descriptive and regression results. Conditional-logit estimates match the published table much more closely when observations are pooled by shared design card, whereas the conventional respondent-by-card choice grouping produces materially different magnitudes and uncertainty. This numerical match does not establish the authors' exact undocumented implementation.

Several published conditional-logit cells and some town-size descriptive shares do not match exactly. Mixed-logit results are also sensitive to simulated integration draws and optimizer behavior. The package reports primary fits, convergence flags, and a 20-seed sensitivity range. Published Figure 2 does not fully align with the model description, so the code provides variants for comparison. We did not obtain the original analysis code, verify the original Stata implementation, contact the authors, or resolve every undocumented analysis choice.

These limitations are reported rather than hidden because the assignment grades reproducibility documentation, not perfect numerical agreement.

## Attribution and AI assistance

The statistical analysis is based on **Team 3's existing ECON 5560 replication work**, not a claim of sole authorship. The upstream team project is documented in `SOURCE_PROVENANCE.md`. Matthew Suban's individual repository was provided as a useful packaging/reference implementation for this assignment; this repository preserves that provenance while creating an independently identified and verified Sam Wegman submission.

AI assistance (ChatGPT/OpenAI) materially helped inspect the assignment, adapt the existing team package, make the repository self-contained, prepare documentation, set up the fresh-checkout verification, inspect the resulting logs, and prepare the Canvas submission text. The underlying statistical estimators and replication targets come from the team project.
