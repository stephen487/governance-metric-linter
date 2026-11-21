# Governance metric linter: flag known-problematic measures in AI governance tools

Licence: MIT (see LICENSE).

## Try it in 10 seconds

From the kit root, with Python 3:

```bash
python demo/run_demo.py
```

It scans `demo/sample_audit.txt`, a short invented audit excerpt, and prints this (the full output is in `demo/EXPECTED_OUTPUT.txt`):

```text
MEASURE           LINE  MATCHED TEXT                                     REGISTRY CONDITIONS (text; citation; url)
four_fifths_rule  9     80% rule                                         Recasting the four-fifths rule as an AI fairness metric introduces new potential for ethical harms. [Watkins, McKenna, Chen (2022). The four-fifths rule is not disparate impact: a woeful tale of epistemic trespassing in algorithmic fairness.; https://arxiv.org/abs/2202.09519]
four_fifths_rule  10    four-fifths rule                                 Recasting the four-fifths rule as an AI fairness metric introduces new potential for ethical harms. [Watkins, McKenna, Chen (2022). The four-fifths rule is not disparate impact: a woeful tale of epistemic trespassing in algorithmic fairness.; https://arxiv.org/abs/2202.09519]
shap              17    SHAP                                             Shapley values used as feature importance raise mathematical problems. [Kumar, Venkatasubramanian, Scheidegger, Friedler (2020). Problems with Shapley-value-based explanations as feature importance measures. ICML.; https://arxiv.org/abs/2002.11097] ; Shapley values miss information about model predictions that the authors' Shapley residuals capture. [Kumar, Scheidegger, Venkatasubramanian, Friedler (2021). Shapley Residuals: Quantifying the limits of the Shapley value for explanations. NeurIPS.; https://nips.cc/virtual/2021/poster/28660] ; Explanation methods that rely on input perturbations, including LIME and SHAP, are not reliable. [Slack, Hilgard, Jia, Singh, Lakkaraju (2020). Fooling LIME and SHAP: Adversarial Attacks on Post hoc Explanation Methods. AIES.; https://arxiv.org/abs/1911.02508] ; Model-agnostic interpretation methods can lead to wrong conclusions when applied incorrectly. [Molnar et al. (2022). General Pitfalls of Model-Agnostic Interpretation Methods for Machine Learning Models.; https://arxiv.org/abs/2007.04131]
shap              20    shap                                             Shapley values used as feature importance raise mathematical problems. [Kumar, Venkatasubramanian, Scheidegger, Friedler (2020). Problems with Shapley-value-based explanations as feature importance measures. ICML.; https://arxiv.org/abs/2002.11097] ; Shapley values miss information about model predictions that the authors' Shapley residuals capture. [Kumar, Scheidegger, Venkatasubramanian, Friedler (2021). Shapley Residuals: Quantifying the limits of the Shapley value for explanations. NeurIPS.; https://nips.cc/virtual/2021/poster/28660] ; Explanation methods that rely on input perturbations, including LIME and SHAP, are not reliable. [Slack, Hilgard, Jia, Singh, Lakkaraju (2020). Fooling LIME and SHAP: Adversarial Attacks on Post hoc Explanation Methods. AIES.; https://arxiv.org/abs/1911.02508] ; Model-agnostic interpretation methods can lead to wrong conclusions when applied incorrectly. [Molnar et al. (2022). General Pitfalls of Model-Agnostic Interpretation Methods for Machine Learning Models.; https://arxiv.org/abs/2007.04131]
shap              21    shap_values                                      Shapley values used as feature importance raise mathematical problems. [Kumar, Venkatasubramanian, Scheidegger, Friedler (2020). Problems with Shapley-value-based explanations as feature importance measures. ICML.; https://arxiv.org/abs/2002.11097] ; Shapley values miss information about model predictions that the authors' Shapley residuals capture. [Kumar, Scheidegger, Venkatasubramanian, Friedler (2021). Shapley Residuals: Quantifying the limits of the Shapley value for explanations. NeurIPS.; https://nips.cc/virtual/2021/poster/28660] ; Explanation methods that rely on input perturbations, including LIME and SHAP, are not reliable. [Slack, Hilgard, Jia, Singh, Lakkaraju (2020). Fooling LIME and SHAP: Adversarial Attacks on Post hoc Explanation Methods. AIES.; https://arxiv.org/abs/1911.02508] ; Model-agnostic interpretation methods can lead to wrong conclusions when applied incorrectly. [Molnar et al. (2022). General Pitfalls of Model-Agnostic Interpretation Methods for Machine Learning Models.; https://arxiv.org/abs/2007.04131]
lime              23    LIME                                             Explanation methods that rely on input perturbations, including LIME and SHAP, are not reliable. [Slack, Hilgard, Jia, Singh, Lakkaraju (2020). Fooling LIME and SHAP: Adversarial Attacks on Post hoc Explanation Methods. AIES.; https://arxiv.org/abs/1911.02508] ; When the explanation is made very local, LIME's surrogate model can degenerate. [Gaudel, Galárraga, Delaunay, Rozé, Bhargava (2022). s-LIME: Reconciling Locality and Fidelity in Linear Explanations. IDA.; https://arxiv.org/abs/2208.01510]
lime              23    local interpretable model-agnostic explanations  Explanation methods that rely on input perturbations, including LIME and SHAP, are not reliable. [Slack, Hilgard, Jia, Singh, Lakkaraju (2020). Fooling LIME and SHAP: Adversarial Attacks on Post hoc Explanation Methods. AIES.; https://arxiv.org/abs/1911.02508] ; When the explanation is made very local, LIME's surrogate model can degenerate. [Gaudel, Galárraga, Delaunay, Rozé, Bhargava (2022). s-LIME: Reconciling Locality and Fidelity in Linear Explanations. IDA.; https://arxiv.org/abs/2208.01510]
```

## The problem

AI governance tools and audit reports often rely on measures that the research literature shows to be unreliable, such as the Four-Fifths rule used outside its legal context, or SHAP and LIME, whose explanations the cited papers show can be unreliable. Nothing checks the choice of measure itself, so a tool can certify a system with a metric that can mislead.

The UK government's roadmap for trusted third-party AI assurance says: "as much as 38% of AI governance tools may utilise metrics that could result in harm". The 38% figure comes from the World Privacy Forum's 2023 report "Risky Analysis: Assessing and Improving AI Governance Tools". That report found more than 38% of the tools it reviewed mention, recommend or incorporate at least one of three measures the literature shows to be problematic. Those three are the four-fifths rule, SHAP and LIME, confirmed from the report's web page. A verbatim read of its PDF footnote is still to be done.

Fairness toolkits compute these measures, but none found in a light search (see EXISTENCE.md) flags their misuse.

## What the base does today

The `base/` folder finds three measures by name in plain text: the four-fifths rule, SHAP and LIME. For each match it reports the measure, the line number, the matched text, and the cited reasons from the registry. Each reason is printed with its text, its citation and a link. The quote is kept in the registry but not printed in the report.

The registry is `base/registry.json`. The base does not decide whether a measure is wrong for a given audit. It reports the cited reasons and leaves the judgement to the reader.

## Quick start

The base uses only the Python standard library. It makes no network call and no model call.

Scan a text file and print the report (run from the kit root):

```bash
python -c "import sys; sys.path.insert(0, '.'); from base.mechanism import scan, report, load_registry; t = open(sys.argv[1], encoding='utf-8').read(); print(report(scan(t), load_registry()))" path/to/audit.txt
```

Run the harness (from the kit root; pytest is required):

```bash
cd harness
python -m pytest -q
```

Exactly 5 tests fail, and every failure says NOT BUILT. Those are the spec tests for the open work below. The failures are expected. All other tests should pass.

## What is left for you

Read `BRIEF.md` for the full idea. The open work, as listed there:

- Read PDF audit reports: extract text with page numbers and report each finding's page.
- Read model cards (Markdown with YAML front matter) and report the section each finding sits in.
- Read fairness-library configs and code (Aequitas, Fairlearn, AI Fairness 360) and flag the measures they compute, not only the words.
- Emit machine-readable output (JSON) so the linter can run in CI and fail a build.
- Tell a measure used as evidence apart from a measure only mentioned (for example in a list of limitations), and report which it is.

## Limits

- Detection is by name only. The base finds the listed names and does not understand how a measure is used. Wrapped phrases and hyphen or space variants match only inside the listed names.
- The acronym and its expansion both match. For example, "local interpretable model-agnostic explanations (LIME)" gives two findings.
- "80% rule" fires in any context, including unrelated uses.
- Lowercase `shap` matches only the library spelling. Titlecase `Shap`, as in a place name, does not match.
- It reads plain text only. It does not parse PDFs, model cards or fairness-library configs.
- The quotes are short excerpts from paper abstracts. They have not yet been checked word for word against the papers.
- Roth et al. (2006) on the 4/5ths rule is cited by the WPF report but not included.

## Layout

- `BRIEF.md` the idea, the obstacle, who would buy it, and quoted sources
- `EXISTENCE.md` what the light search found, and its caveats
- `base/` the smallest proof of the mechanism, and the registry
- `harness/` tests that define done
- `LICENSE` MIT
- `CONTRIBUTING.md` how to carry this on
