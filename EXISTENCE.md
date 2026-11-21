# Existence check: governance-metric-linter

Light search, 21 November 2026.

## Verdict

GAP (narrow). No tool was found that checks whether a governance tool's chosen measure is a known-problematic one.

## What exists

- Fairness toolkits compute these measures, including Four-Fifths-style disparate impact ratios: Aequitas, AI Fairness 360, Fairlearn, audit-ai, Credo AI Lens and VerifyML. None of them was found to warn that a ratio is being used outside its validity.
- Hugging Face Evaluate has per-metric documentation with "pitfalls". That is documentation, not an automated check.
- Narrow linters: evallint (lints evaluation sets for duplicates; its page did not load, so it is not verified) and metrictrust (flags noisy fine-tuning validation numbers). Neither checks the choice of measure.

## The evidence base

The World Privacy Forum's December 2023 report, "Risky Analysis: Assessing and Improving AI Governance Tools", says more than 38% of the tools it reviewed mention, recommend or incorporate at least one of three measures the literature shows to be problematic.
Source: https://www.worldprivacyforum.org/2023/12/new-report-risky-analysis-assessing-and-improving-ai-governance-tools/

## The three measures

1. The US Four-Fifths (80%) rule, used for AI fairness and disparate impact outside its employment-law context.
2. SHAP.
3. LIME.

The report's section headings and its appendix match these three. Counts recorded in the OECD AI tools catalogue: SHAP 9 items, LIME 3, Four-Fifths 3.

## Papers the registry is filled from

Titles and years only:

- The Four-Fifths Rule is Not Disparate Impact: A Woeful Tale of Epistemic Trespassing in Algorithmic Fairness (2022)
- Modeling the Behavior of the 4/5ths Rule for Determining Adverse Impact: Reasons for Caution (2006). Cited by the report, not yet read, not in the registry.
- Problems with Shapley-value-based explanations as feature importance measures (2020)
- Shapley Residuals: Quantifying the limits of the Shapley value for explanations (2021)
- Fooling LIME and SHAP: Adversarial Attacks on Post hoc Explanation Methods (2020)
- General Pitfalls of Model-Agnostic Interpretation Methods for Machine Learning Models (2022)
- s-LIME: Reconciling Locality and Fidelity in Linear Explanations (2022)

## Caveats

- Three web searches only. This is a light check, not a full literature search.
- No GitHub code search for four-fifths or 80% rule warnings inside fairness libraries was done.
- evallint's page did not load, so it is not verified.
- The report is a review, not a tool. No downloadable checklist was found.
- The three measures are confirmed from a summarised read of the report's web page. The PDF footnote that carries the 38% sentence has not been read verbatim, and neither has Appendix C.
