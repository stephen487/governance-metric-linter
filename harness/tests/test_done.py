"""Harness for the governance metric linter seed. These tests define "done" for the base.

- Detection: an audit-report-like fixture yields exactly the expected findings and line numbers.
- Must-fire: each listed phrase or code form fires, including wrapped and hyphen or space variants.
- Hard negatives: near-miss twins that must NOT fire.
- Registry: every listed name fires on itself; every condition is cited.
- Report: each finding's measure id and line number appear in the output.
- What is left: one NOT BUILT test per open item in BRIEF.md.
"""
import pathlib

import pytest

from base import mechanism
from base.mechanism import Finding, load_registry, report, scan


AUDIT_FIXTURE = """Audit report: loan approval model, version 2.
Fairness: approval rates were compared with the four-fifths rule.
Explanations were produced with SHAP for every applicant.
Local behaviour was also checked with LIME.
The disparate impact ratio for group B was 0.83.
Group C passes the 80% rule on this sample.
Explanations used local interpretable model-agnostic explanations as a second method.
Summary: 80% of the rules were reviewed by hand.
"""

EXPECTED_FIXTURE_FINDINGS = [
    ("four_fifths_rule", "four-fifths rule", 2),
    ("shap", "SHAP", 3),
    ("lime", "LIME", 4),
    ("four_fifths_rule", "disparate impact ratio", 5),
    ("four_fifths_rule", "80% rule", 6),
    ("lime", "local interpretable model-agnostic explanations", 7),
]

HARD_NEGATIVES = [
    "lime green",
    "Lime Street",
    "shapely",
    "the shape of",
    "80% of the rules",
    "a score of 80%",
    "four-fifths of respondents agreed",
    "SHAPE",
    "LIMEstone",
    "80%",
    "shape",
    "a shapshot",
    "lime juice",
    "TreeSHAPE",
    "Shap Street",
    "Shap village",
    "the A6 over Shap",
    "the lime in the drink",
    "a lime tree",
    "limestone",
    "juice from lime",
    "made from lime and salt",
]

# (text, measure_id, matched_text). Each entry is one test case.
MUST_FIRE = [
    # earlier rounds
    ("we used shap values", "shap", "shap"),
    ("import shap", "shap", "shap"),
    ("KernelSHAP was run on the sample", "shap", "KernelSHAP"),
    ("TreeSHAP explainer", "shap", "TreeSHAP"),
    ("DeepSHAP attributions", "shap", "DeepSHAP"),
    ("LinearSHAP baseline", "shap", "LinearSHAP"),
    ("GradientSHAP values", "shap", "GradientSHAP"),
    ("the eighty percent rule", "four_fifths_rule", "eighty percent rule"),
    ("the eighty per cent rule", "four_fifths_rule", "eighty per cent rule"),
    ("the 80 per cent rule", "four_fifths_rule", "80 per cent rule"),
    # round 6: wrapped and hyphen or space variants
    ("the four-fifths\nrule was applied", "four_fifths_rule", "four-fifths\nrule"),
    ("the four-fifths rule was applied", "four_fifths_rule", "four-fifths rule"),
    ("the four fifths rule was applied", "four_fifths_rule", "four fifths rule"),
    ("the 80-percent rule", "four_fifths_rule", "80-percent rule"),
    ("the 80 percent rule", "four_fifths_rule", "80 percent rule"),
    ("the eighty-percent rule", "four_fifths_rule", "eighty-percent rule"),
    ("the 80-per-cent rule", "four_fifths_rule", "80-per-cent rule"),
    ("the 80 % rule", "four_fifths_rule", "80 % rule"),
    ("the four-fifth rule", "four_fifths_rule", "four-fifth rule"),
    ("the 4/5 rule", "four_fifths_rule", "4/5 rule"),
    ("the 4/5th rule", "four_fifths_rule", "4/5th rule"),
    ("the adverse impact ratio", "four_fifths_rule", "adverse impact ratio"),
    (
        "local interpretable model agnostic explanations",
        "lime",
        "local interpretable model agnostic explanations",
    ),
    (
        "a local  interpretable\nmodel-agnostic explanations",
        "lime",
        "local  interpretable\nmodel-agnostic explanations",
    ),
    # round 6: SHAP additions
    ("the Shapley value of each feature", "shap", "Shapley value"),
    ("the Shapley values of each feature", "shap", "Shapley values"),
    ("we used shap_values", "shap", "shap_values"),
    # round 6: LIME code forms
    ("import lime", "lime", "import lime"),
    ("from lime import lime_tabular", "lime", "from lime import"),
    ("lime_tabular", "lime", "lime_tabular"),
    ("lime_image", "lime", "lime_image"),
    ("lime_text", "lime", "lime_text"),
    ("LimeTabularExplainer", "lime", "LimeTabularExplainer"),
    ("LimeImageExplainer", "lime", "LimeImageExplainer"),
    ("LimeTextExplainer", "lime", "LimeTextExplainer"),
]


# --- base is importable -------------------------------------------------------

def test_base_is_importable():
    assert mechanism is not None


def test_registry_loads_three_measures():
    ids = [m["id"] for m in load_registry()["measures"]]
    assert ids == ["four_fifths_rule", "shap", "lime"]


# --- detection on the fixture ------------------------------------------------

def test_fixture_yields_exactly_the_expected_findings_and_lines():
    findings = scan(AUDIT_FIXTURE)
    assert all(isinstance(f, Finding) for f in findings)
    got = [(f.measure_id, f.matched_text, f.line) for f in findings]
    assert got == EXPECTED_FIXTURE_FINDINGS


def test_char_start_points_at_the_matched_text():
    for f in scan(AUDIT_FIXTURE):
        assert AUDIT_FIXTURE[f.char_start:f.char_start + len(f.matched_text)] == f.matched_text


# --- must fire: one test per case --------------------------------------------

@pytest.mark.parametrize("text, measure_id, matched", MUST_FIRE)
def test_must_fire(text, measure_id, matched):
    got = [(f.measure_id, f.matched_text) for f in scan(text)]
    assert (measure_id, matched) in got, f"expected {(measure_id, matched)} in {got}"


# --- hard negatives: twins that must NOT fire --------------------------------

@pytest.mark.parametrize("text", HARD_NEGATIVES)
def test_hard_negative_does_not_fire(text):
    assert scan(text) == []


# --- every listed name fires on itself ---------------------------------------

NAME_PAIRS = [(e["id"], n) for e in load_registry()["measures"] for n in e["names"]]


@pytest.mark.parametrize("measure_id, name", NAME_PAIRS)
def test_every_registry_name_fires_on_itself(measure_id, name):
    got = [(f.measure_id, f.matched_text) for f in scan(f"We used {name} in the audit.")]
    assert (measure_id, name) in got, f"{name!r} does not fire on itself: {got}"


# --- registry guard: every condition is cited --------------------------------

REQUIRED_FIELDS = {"text", "citation", "url", "quote"}


@pytest.mark.parametrize("entry", load_registry()["measures"], ids=lambda e: e["id"])
def test_registry_entry_has_at_least_one_condition(entry):
    assert len(entry["conditions"]) >= 1, f"{entry['id']} has no condition"


@pytest.mark.parametrize("entry", load_registry()["measures"], ids=lambda e: e["id"])
def test_every_registry_condition_is_cited(entry):
    for cond in entry["conditions"]:
        assert REQUIRED_FIELDS <= set(cond), f"{entry['id']}: missing keys {sorted(REQUIRED_FIELDS - set(cond))}"
        for key in ("text", "citation", "quote"):
            assert cond[key].strip(), f"{entry['id']}: empty {key}"
            assert "TO FILL" not in cond[key], f"{entry['id']}: {key} is still TO FILL: {cond[key]!r}"
        assert cond["url"].startswith("https://"), f"{entry['id']}: url must start with https://: {cond['url']!r}"
        assert "TO FILL" not in cond["url"], f"{entry['id']}: url is still TO FILL"


@pytest.mark.parametrize("entry", load_registry()["measures"], ids=lambda e: e["id"])
def test_no_two_conditions_in_an_entry_share_a_quote(entry):
    quotes = [c["quote"] for c in entry["conditions"]]
    assert len(quotes) == len(set(quotes)), f"{entry['id']}: duplicate quote across conditions"


# --- report ------------------------------------------------------------------

def test_report_has_measure_id_and_line_for_each_finding():
    registry = load_registry()
    findings = scan(AUDIT_FIXTURE)
    out = report(findings, registry)
    rows = out.splitlines()
    for f in findings:
        assert any(row.split()[:2] == [f.measure_id, str(f.line)] for row in rows), (
            f"report has no row for {f.measure_id} on line {f.line}:\n{out}"
        )


def test_report_shows_citation_and_url_for_each_condition():
    registry = load_registry()
    findings = scan(AUDIT_FIXTURE)
    out = report(findings, registry)
    for f in findings:
        for cond in next(m for m in registry["measures"] if m["id"] == f.measure_id)["conditions"]:
            assert cond["citation"] in out, f"citation missing from report: {cond['citation']!r}"
            assert cond["url"] in out, f"url missing from report: {cond['url']!r}"


def test_report_with_no_findings_says_so():
    assert "No registry measures found" in report([], load_registry())


# --- demo: the recorded demo output must match a fresh scan ------------------

DEMO_DIR = pathlib.Path(__file__).resolve().parents[2] / "demo"


def test_demo_scan_matches_expected_output():
    text = (DEMO_DIR / "sample_audit.txt").read_text(encoding="utf-8")
    got = sorted((f.measure_id, f.line) for f in scan(text))
    expected = []
    for row in (DEMO_DIR / "EXPECTED_OUTPUT.txt").read_text(encoding="utf-8").splitlines():
        parts = row.split()
        if len(parts) >= 2 and parts[1].isdigit():
            expected.append((parts[0], int(parts[1])))
    assert got == sorted(expected), f"demo drifted. fresh scan: {got}; recorded: {sorted(expected)}"


# --- what is left (BRIEF.md): one NOT BUILT test per open item ----------------

def not_built(what):
    pytest.fail("NOT BUILT: " + what)


def test_whats_left_pdf_audit_reports():
    not_built("Read PDF audit reports: extract text with page numbers and report each finding's page.")


def test_whats_left_model_cards():
    not_built("Read model cards (Markdown with YAML front matter) and report the section each finding sits in.")


def test_whats_left_fairness_library_configs():
    not_built("Read fairness-library configs and code (Aequitas, Fairlearn, AI Fairness 360) and flag the measures they compute, not only the words.")


def test_whats_left_machine_readable_output():
    not_built("Emit machine-readable output (JSON) so the linter can run in CI and fail a build.")


def test_whats_left_evidence_vs_mention():
    not_built("Tell a measure used as evidence apart from a measure only mentioned (for example in a list of limitations), and report which it is.")
