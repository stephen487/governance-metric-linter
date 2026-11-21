# base/

Stdlib only. No network call, no model call.

- `registry.json` lists three measures (four-fifths rule, SHAP, LIME), the names that identify each one, and cited conditions for each. Every condition has a text, a citation, a url and a short quote.
- `mechanism.py` has `scan(text)`, which searches the whole text and returns a `Finding` (measure, matched text, line, character offset) for each registry name it finds. Line numbers are computed from the match position.
- `mechanism.py` has `report(findings, registry)`, which prints a plain-text table with one row per finding, showing each condition's text, citation and url. The quote is not printed.

How names match:

- Single words spelled all-upper (SHAP, LIME) or all-lower (shap) match exactly as written. So `Shap` as a place name does not match.
- The two names listed under `exact_names` in `registry.json` (`import lime`, `from lime import`) also match exactly as written.
- Every other name matches case-insensitively.
- Inside a multi-word name, any run of whitespace and/or hyphens counts as one separator. A phrase wrapped across a line break still matches.

Sources:

- The conditions are cited from the papers that the World Privacy Forum 2023 report "Risky Analysis" cites.
- The quotes are short excerpts from each paper's abstract, as supplied. They have not yet been checked word for word against the papers.
- Roth et al. (2006) on the four-fifths rule is cited by the same report but not yet read, so it is not in the registry.

What it does not do:

- It does not parse PDFs, model cards or fairness-library configs. It reads plain text only.
- It does not judge whether a measure is unreliable. It reports the registry's cited conditions for a measure that appears in the text. Whether a condition applies to a given audit is left to the reader.
- It does not check how a measure is used. It only finds the name.

The harness in `../harness/` holds the detection fixtures, the must-fire and hard-negative cases, the registry guard, and the open items as NOT BUILT tests.
