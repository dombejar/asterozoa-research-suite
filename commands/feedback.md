---
description: Turn freeform run feedback into categorized next-run changes for the research or model skills.
---

Process feedback: $ARGUMENTS

Load the feedback prompt at ${CLAUDE_PLUGIN_ROOT}/skills/securities-research/reference/feedback-prompt.md and apply it to the freeform input above.

The feedback prompt will categorize the input into structured next-run changes (e.g. sourcing gaps, stance adjustments, model scope changes, formatting fixes) so they can be applied on the next research or model-building run.

Output the categorized change list. Do not apply changes inline — surface them for review first.
