"""Run the linter on the sample audit report and print the report.

Run from the kit root:  python demo/run_demo.py
Stdlib only. No network call, no model call.
"""
import pathlib
import sys

KIT_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KIT_ROOT))

from base.mechanism import load_registry, report, scan  # noqa: E402

SAMPLE = KIT_ROOT / "demo" / "sample_audit.txt"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    text = SAMPLE.read_text(encoding="utf-8")
    print(report(scan(text), load_registry()), end="")


if __name__ == "__main__":
    main()
