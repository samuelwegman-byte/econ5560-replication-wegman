"""Rebuild the complete Team 3 replication from the unchanged public raw data."""
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path
import hashlib
import json
import os
import platform
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
STEPS = [
    "01_parse_data.py", "02_descriptives.py", "03_conditional_logit.py",
    "04_mixed_logit.py", "05_build_dashboard.py", "06_slide_figures.py",
    "07_paper_figures.py", "08_debug_discrepancies.py",
]
RAW_SHA256 = "ea292824db6b36ef18961aa954f0cb7964af5a7285d7e479840cf7aef19f3df2"
PACKAGES = ["numpy", "pandas", "scipy", "statsmodels", "matplotlib"]


def main():
    started = time.perf_counter()
    raw = ROOT / "data/raw/S1Table.DTA"
    if hashlib.sha256(raw.read_bytes()).hexdigest() != RAW_SHA256:
        raise ValueError("Raw data checksum differs from the original PLOS download")
    (ROOT / "logs").mkdir(exist_ok=True)
    print("ECON 5560 replication | samuelwegman-byte", flush=True)
    print(f"Started UTC: {datetime.now(timezone.utc).isoformat()}", flush=True)
    print("Raw data SHA-256 verified", flush=True)
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    env["MPLBACKEND"] = "Agg"
    for step in STEPS:
        stage_start = time.perf_counter()
        print(f"\n>>> {step}", flush=True)
        subprocess.run(
            [sys.executable, "-u", str(ROOT / "scripts" / step)],
            cwd=ROOT / "scripts", env=env, check=True,
        )
        print(f"<<< {step} completed in {time.perf_counter() - stage_start:.2f} seconds", flush=True)

    # Check the products rather than accepting a zero exit status alone.
    import numpy as np
    import pandas as pd
    long = pd.read_csv(ROOT / "outputs/data/choice_long.csv")
    complete = long[long.complete == 1]
    assert len(complete) == 1968 and complete.id.nunique() == 164
    assert len(complete[complete.councillor == 1]) == 1476
    assert complete.groupby(["id", "choice_set"]).chosen.sum().eq(1).all()
    for table, rows in [("table3_cl.csv", 24), ("table3_ml.csv", 24)]:
        frame = pd.read_csv(ROOT / "outputs/tables" / table)
        assert len(frame) == rows
        assert np.isfinite(frame.select_dtypes(include="number").to_numpy()).all()
    for exhibit in (ROOT / "scripts/replication-targets").glob("*.png"):
        assert (ROOT / "outputs/paper_figures" / exhibit.name).stat().st_size > 0
    dashboard = (ROOT / "outputs/dashboard/index.html").read_text()
    assert "/*__DATA__*/null" not in dashboard
    ml = json.loads((ROOT / "outputs/results/ml.json").read_text())
    convergence = {key: ml[key]["primary"]["converged"] for key in ("m3", "m4")}
    elapsed = time.perf_counter() - started
    report = {
        "status": "PASS", "completed_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": round(elapsed, 2), "raw_sha256": RAW_SHA256,
        "complete_respondents": 164, "complete_rows": 1968,
        "councillor_rows": 1476, "primary_mixed_logit_converged": convergence,
        "python": platform.python_version(),
        "packages": {name: version(name) for name in PACKAGES},
    }
    (ROOT / "logs/run_summary.json").write_text(json.dumps(report, indent=2) + "\n")
    manifest = []
    for path in sorted((ROOT / "outputs").rglob("*")):
        if path.is_file():
            manifest.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(ROOT).as_posix()}")
    (ROOT / "logs/output_sha256.txt").write_text("\n".join(manifest) + "\n")
    git = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True)
    # The final 20 lines form the requested Canvas excerpt and record the environment.
    print("\n" + "\n".join([
        "=== FINAL RUN AND ENVIRONMENT SUMMARY ===",
        "Pipeline status: PASS (all eight stages completed)",
        "Output validation: PASS (samples, choices, numeric tables, exhibits, dashboard)",
        "GitHub username: samuelwegman-byte",
        "Repository: https://github.com/samuelwegman-byte/econ5560-replication-wegman",
        f"Source commit: {git.stdout.strip() if git.returncode == 0 else 'unavailable'}",
        f"Completed UTC: {report['completed_utc']}",
        f"Full pipeline elapsed: {elapsed:.2f} seconds",
        f"Python: {platform.python_version()} ({platform.python_implementation()})",
        f"Operating system: {platform.platform()}",
        *[f"{name}: {version(name)}" for name in PACKAGES],
        f"Raw data SHA-256: {RAW_SHA256}",
        f"Regenerated output files: {len(manifest)}",
        f"Mixed logit primary convergence: m3={convergence['m3']}, m4={convergence['m4']}",
        "Limitations: published cells differ; mixed-logit results depend on simulation draws.",
        "=== END ENVIRONMENT SUMMARY ===",
    ]), flush=True)


if __name__ == "__main__":
    main()
