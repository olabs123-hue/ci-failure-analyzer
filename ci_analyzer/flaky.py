"""Detect inconsistent outcomes for the same test at the same revision."""
from collections import defaultdict

def detect_flaky(records):
    groups = defaultdict(list)
    for record in records:
        if not all(k in record for k in ("test_id", "revision", "status")):
            raise ValueError("Each record needs test_id, revision and status")
        if record["status"] not in ("pass", "fail"):
            raise ValueError("status must be pass or fail")
        groups[(record["test_id"], record["revision"])].append(record["status"])
    return [{"test_id": test, "revision": revision, "runs": len(statuses),
             "passes": statuses.count("pass"), "failures": statuses.count("fail")}
            for (test, revision), statuses in sorted(groups.items())
            if "pass" in statuses and "fail" in statuses]
