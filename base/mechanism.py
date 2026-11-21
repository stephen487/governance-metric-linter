"""Seed mechanism: find named measures in a text and report them with their registry conditions.

Stdlib only. No network call, no model call.

The registry (registry.json) conditions are cited from the papers, one citation and url per condition.
This module finds measures by their listed names only and reports the registry entry. It does not
judge a measure.
"""
from dataclasses import dataclass
import json
import pathlib
import re

REGISTRY_PATH = pathlib.Path(__file__).with_name("registry.json")


@dataclass(frozen=True)
class Finding:
    measure_id: str
    matched_text: str
    line: int
    char_start: int


def load_registry(path=REGISTRY_PATH):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _is_case_sensitive(name):
    # A single word spelled all-upper (SHAP, LIME) or all-lower (shap) matches exactly as written.
    # Titlecase words such as "Shap" do not match it.
    return name.isalpha() and (name.isupper() or name.islower())


def _pattern_for(name, exact_names):
    # Names listed in exact_names match exactly as written, as do single words spelled all-upper
    # or all-lower. Every other name matches case-insensitively.
    # Inside a multi-word name, any run of whitespace and/or hyphens counts as one separator, so a
    # phrase wrapped across a line break still matches. The lookarounds keep a match to whole names.
    words = [w for w in re.split(r"[\s\-]+", name) if w]
    body = r"[\s\-]+".join(re.escape(w) for w in words)
    flags = 0 if (name in exact_names or _is_case_sensitive(name)) else re.IGNORECASE
    return re.compile(r"(?<!\w)" + body + r"(?!\w)", flags)


def scan(text):
    """Return one Finding per match of a registry name in the whole text, ordered by position."""
    registry = load_registry()
    findings = []
    seen = set()
    for entry in registry["measures"]:
        exact_names = set(entry.get("exact_names", []))
        for name in entry["names"]:
            for m in _pattern_for(name, exact_names).finditer(text):
                spot = (entry["id"], m.start())
                if spot in seen:
                    continue
                seen.add(spot)
                line = text.count("\n", 0, m.start()) + 1
                findings.append(Finding(entry["id"], m.group(0), line, m.start()))
    ordered = sorted((f.char_start, n, f) for n, f in enumerate(findings))
    return [f for _, _, f in ordered]


def report(findings, registry):
    """Plain-text table: one row per finding, with each registry condition's text, citation and url."""
    if not findings:
        return "No registry measures found.\n"
    conditions = {m["id"]: m["conditions"] for m in registry["measures"]}
    rows = [("MEASURE", "LINE", "MATCHED TEXT", "REGISTRY CONDITIONS (text; citation; url)")]
    for f in findings:
        conds = " ; ".join(
            f"{c['text']} [{c['citation']}; {c['url']}]" for c in conditions.get(f.measure_id, [])
        )
        # A wrapped match shows on one line: whitespace (including a line break) becomes a single space.
        rows.append((f.measure_id, str(f.line), " ".join(f.matched_text.split()), conds))
    w0 = max(len(r[0]) for r in rows)
    w1 = max(len(r[1]) for r in rows)
    w2 = max(len(r[2]) for r in rows)
    out = []
    for r in rows:
        out.append(f"{r[0].ljust(w0)}  {r[1].ljust(w1)}  {r[2].ljust(w2)}  {r[3]}".rstrip())
    return "\n".join(out) + "\n"
