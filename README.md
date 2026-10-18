# CI Failure Analyzer — NVIDIA AI CI/CD Infrastructure Portfolio Project

An **offline, explainable Python CI triage tool** for compiler/build pipelines. Classifies failures into `compiler_error`, `dependency_error`, `infrastructure_error`, `timeout`, `test_failure`, or `unknown`; surfaces evidence and manual-review flags; detects tests that both pass and fail **at the same revision**; and evaluates classification accuracy against labelled examples.

**Important:** This version is a deterministic rule-based baseline, **not an AI/ML model**. It is designed to support a future AI classifier and provide a measurable baseline without making unsupported AI claims. The sample logs are synthetic and not NVIDIA production data.

## Run (Python 3.9+, no third-party runtime dependencies)

```bash
python -m unittest discover -s tests -v
python -m ci_analyzer.cli classify examples/compiler.log
python -m ci_analyzer.cli evaluate examples/labeled_logs.json
python -m ci_analyzer.cli flaky examples/test_runs.json
```

Or install: `python -m pip install -e .` and use `ci-analyze classify examples/compiler.log`.

## Approach

- **Classification:** Regular-expression signatures with evidence, confidence heuristics, and manual review for unknown/ambiguous cases. Not calibrated probabilities.
- **Flaky detection:** A test is flagged only if it has pass and fail outcomes on the same commit revision; this is a *flakiness signal*, not proof of nondeterminism.
- **Evaluation:** Accuracy and per-class precision/recall on labelled JSON. The small included synthetic dataset demonstrates the pipeline, **not real-world generalization**.
- **CI:** GitHub Actions executes unit tests and the example evaluation on Python 3.9, 3.11, 3.12.

## Roadmap for genuine AI assistance

1. Gather consented, anonymized compiler CI logs; scrub secrets and tokens.
2. Split train/test data by repository and time to avoid leakage.
3. Train a text classifier (e.g., TF-IDF + logistic regression) and compare against this baseline.
4. Evaluate macro-F1, false positives, latency and human-review rates.
5. Add a human-in-the-loop feedback queue and track model drift.

## Responsible claims

Only report metrics generated from actual runs. Do not represent synthetic examples as NVIDIA CI data, or this baseline as a deployed AI model.
