"""Deterministic, explainable log classifier; no external model/API required."""
import re
from dataclasses import dataclass, asdict

PATTERNS = {
    "compiler_error": [r"\berror:.*(?:undeclared|undefined|expected|invalid|no matching|cannot convert)", r"\bfatal error:.*(?:file not found|no such file)", r"\bundefined reference to\b", r"\bLLVM ERROR:"],
    "dependency_error": [r"ModuleNotFoundError", r"No module named", r"Could not find a package configuration file", r"\bdependency resolution failed\b", r"\bpackage .* not found\b"],
    "infrastructure_error": [r"connection (?:timed out|refused|reset)", r"\bHTTP (?:502|503|504)\b", r"no space left on device", r"runner lost communication", r"\bnetwork is unreachable\b"],
    "test_failure": [r"\bAssertionError\b", r"\bFAILED tests/", r"\bexpected .* but got\b", r"\btests? failed\b", r"\bFAIL: "],
    "timeout": [r"\b(?:job|test|command) timed out\b", r"\btimeout(?:error|exception)\b", r"exceeded time limit"],
}
PRIORITY = ["compiler_error", "dependency_error", "infrastructure_error", "timeout", "test_failure"]

@dataclass
class Classification:
    category: str
    confidence: float
    evidence: list
    needs_review: bool

    def to_dict(self):
        return asdict(self)

def classify(log: str) -> Classification:
    matches = {}
    for category, patterns in PATTERNS.items():
        evidence = []
        for pattern in patterns:
            match = re.search(pattern, log, flags=re.IGNORECASE | re.MULTILINE)
            if match:
                evidence.append(match.group(0)[:140])
        if evidence:
            matches[category] = evidence
    if not matches:
        return Classification("unknown", 0.0, [], True)
    chosen = max(PRIORITY, key=lambda c: (len(matches.get(c, [])), -PRIORITY.index(c)))
    if chosen not in matches:
        return Classification("unknown", 0.0, [], True)
    ambiguous = len(matches) > 1
    confidence = min(0.95, 0.65 + 0.1 * (len(matches[chosen]) - 1))
    if ambiguous:
        confidence = min(confidence, 0.55)
    return Classification(chosen, round(confidence, 2), matches[chosen], ambiguous or confidence < 0.6)
