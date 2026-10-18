# Local verification report

Date: 2026-10-18

- Python unit tests: **13/13 passed**, using `python -m unittest discover -s tests -v`.
- Synthetic labelled examples: **16/16 correct (100% accuracy)**, using `python -m ci_analyzer.cli evaluate examples/labeled_logs.json`.
- Flaky-test demonstration: detected `llvm_codegen_x86` at revision `abc123` (2 passes, 1 failure in 3 runs).
- Sample compiler-log classification: `compiler_error`.

**Scope:** These results were measured locally on intentionally small, synthetic fixtures. They do **not** measure accuracy on production CI logs, real AI/ML classification, or performance improvement in NVIDIA infrastructure. The GitHub Actions workflow is included but has not been executed on GitHub.
