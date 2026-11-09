# Fresh-checkout verification

This repository was checked out by GitHub Actions into a clean hosted runner.

- Workflow run: https://github.com/samuelwegman-byte/econ5560-replication-wegman/actions/runs/42566907774
- Source commit before generated files were committed: 00e809df9b1cac814517173d02e9c4ffab8b9dba
- Status: PASS
- Full pipeline elapsed: 636.26 seconds
- Python: 3.12.16
- Complete respondents: 164
- Complete alternative rows: 1968
- Councillor rows: 1476
- Mixed-logit convergence: {'m3': True, 'm4': True}

The workflow deleted any existing outputs before running, installed pinned dependencies, ran python run_all.py, captured stdout/stderr to logs/run_log.txt, and regenerated the outputs from the raw data.
