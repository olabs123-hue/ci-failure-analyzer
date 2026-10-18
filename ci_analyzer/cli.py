import argparse
import json
from pathlib import Path
from .classifier import classify
from .flaky import detect_flaky
from .evaluate import evaluate

def main():
    parser = argparse.ArgumentParser(description="Offline CI failure triage")
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("classify", "flaky", "evaluate"):
        p = sub.add_parser(command)
        p.add_argument("file", type=Path)
        p.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.command == "classify":
        result = classify(args.file.read_text(encoding="utf-8", errors="replace")).to_dict()
    else:
        data = json.loads(args.file.read_text(encoding="utf-8"))
        result = detect_flaky(data) if args.command == "flaky" else evaluate(data, classify)
    rendered = json.dumps(result, indent=2)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)

if __name__ == "__main__":
    main()
