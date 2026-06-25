---
description: Research ticker(s) using primary-source-first securities research (EDGAR-first, every claim source-tagged).
---

Research ticker(s): $ARGUMENTS

Load and follow the skill at ${CLAUDE_PLUGIN_ROOT}/skills/securities-research/SKILL.md.

Default mode: --mode exec-summary --connectors edgar-only

Available modes: bullet | exec-summary | full

Rules:
- Primary sources (EDGAR filings, company IR, official disclosures) come first; secondary sources only to fill gaps.
- Every factual claim must be source-tagged with the document, filing, or URL it came from.
- Lead with Key Insights section; take a clear analytical stance on the security: mispriced or not, which instrument best expresses the view, what evidence would flip the read. No hedge-everything summaries. The reader makes the allocation decision.
- If $ARGUMENTS specifies a mode or connector flag, use that instead of the default.
