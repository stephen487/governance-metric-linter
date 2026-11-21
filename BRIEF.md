# Governance metric linter: flag known-problematic measures in AI governance tools

slug: governance-metric-linter
status: DRAFT

## Technical obstacle
AI governance tools and audit reports often rely on measures that the research literature shows to be unreliable, such as the Four-Fifths rule used outside its legal context or SHAP and LIME, whose explanations the cited papers show can be unreliable. Nothing checks the choice of measure itself, so a tool can certify a system with a metric that can mislead.

## Mechanism
Read an audit report, model card or governance tool config, detect each measure it uses, and look it up in a small registry of known-problematic measures. Each registry entry holds the conditions under which the measure is unreliable and the evidence for them. The output is a per-measure finding: measure, where it was found, which condition applies, and the citation. The base proves detection and lookup on fixture documents with no model call.

## Who would buy it
Third-party AI assurance providers and in-house compliance teams who must defend their choice of metrics to a regulator or client. Not yet researched: no buyer has been asked.

## Sources quoted
- https://www.gov.uk/government/publications/trusted-third-party-ai-assurance-roadmap/trusted-third-party-ai-assurance-roadmap
  > "as much as 38% of AI governance tools may utilise metrics that could result in harm"

## What's left for you
- Read PDF audit reports: extract text with page numbers and report each finding's page.
- Read model cards (Markdown with YAML front matter) and report the section each finding sits in.
- Read fairness-library configs and code (Aequitas, Fairlearn, AI Fairness 360) and flag the measures they compute, not only the words.
- Emit machine-readable output (JSON) so the linter can run in CI and fail a build.
- Tell a measure used as evidence apart from a measure only mentioned (for example in a list of limitations), and report which it is.

## Existence
GAP (narrow), light search 2026-11-21: fairness toolkits compute these measures, but none found in that search flags their misuse. Findings and caveats: EXISTENCE.md
