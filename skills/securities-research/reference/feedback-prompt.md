# D4: Post-Run Feedback Intake Prompt

This artifact extends a post-execution assumption-delta pattern to the securities-research loop. It borrows the four-bucket delta structure (Correct / Corrected / Killed → real / Stays dead) and maps each bucket to five named Feedback Levers (FL1-FL5). The primary invocation point is Phase 4 (Monitor), but the prompt is usable after any research loop phase.

**Framing:** This is an AUGMENTATION tool. It helps the analyst articulate what was off so the next run is better calibrated. It does not replace the analyst's judgment or auto-update the skill unilaterally. All durable-skill-update proposals require explicit human approval before any file is edited.

---

## How to Use

1. Paste this file into a chat session.
2. Fill in the Structured Intake Header fields below.
3. Paste your freeform feedback below the header.
4. The model routes each complaint to a Feedback Lever (FL1-FL5) and fills the four delta buckets.
5. Review the durable-skill-update proposals and surface to the human owner for approval before any file is changed.

No tooling, API authentication, or harness dependency required.

---

## Structured Intake Header

Fill all fields before pasting freeform feedback. The "Specific section(s)" field is required: it anchors ambiguous feedback to the right lever.

```
Ticker / Name:
Run date:
Loop phase: [Sourcing / Deep Dive / IC Memo / Monitor / Exit]
Depth path taken: [DEEP / LIGHT / not stated]
Output artifact(s) reviewed: [synthesis.md / ic-memo.md / chat-elevator.md / model.md / ingestion.md]
Specific section(s) the analyst is reacting to: (required: name the section before pasting freeform text,
  e.g., "synthesis section 3 variant view" or "IC memo section 6 valuation".
  This prevents feedback from routing to the wrong lever.)
```

**Freeform feedback (paste below this line):**

---

## Feedback Lever Table (FL1-FL5)

Route each feedback phrase to the lever(s) it activates. When feedback matches no lever, use the Unclassified row.

| Lever | What it controls | Language patterns that activate it | Output artifact / file touched when it fires |
|-------|-----------------|-------------------------------------|----------------------------------------------|
| **FL1** | Depth-path decision (DEEP vs LIGHT). Governs how much cap-structure, scenario-tree, and liquidity-runway work is added. | "went too deep for this name", "overkill", "didn't need the full scenario tree", "liquidity obviously not binding" | `reference/research-loop.md` (depth-path default for name class) |
| **FL2** | Granularity toggles: segment-level, property-level, per-unit operating data. Governs how deep ingestion goes within an earnings call or IR deck. | "don't trust the segment split", "where did that number come from", "needed more granularity at the property level", "missing per-unit data", "needed unit-level store data" (retail), "needed per-location traffic data" (restaurant chains) | `reference/research-loop.md` (sourcing instruction for granularity level) |
| **FL3** | Source-tier discipline: which tiers were consulted and whether Tier-2/3 contamination appeared in a Tier-1-presenting claim. | "I don't trust that source", "where did that number come from", "that wasn't in the transcript", "Tier-2 number in a Tier-1 claim" | `reference/output-templates.md` (source-tag grammar), `reference/research-loop.md` (re-pull instruction) |
| **FL4** | Length/compression mode: full synthesis vs IC memo vs chat elevator. The output artifact selected for this run. | "too long", "I didn't need all this", "just needed the chat elevator", "could have been shorter", "too much detail for this stage" | `reference/output-templates.md` (default artifact for phase/name-class) |
| **FL5** | Framing voice: augmentation-aid register vs replacement-tool register. The tone and claimed scope of the output. | "framing felt like it was replacing my judgment", "felt like it was telling me what to think", "too prescriptive", "sounded like a decision, not an analysis" | `reference/framework.md` (augmentation posture section) |
| **Unclassified** | Feedback that matches none of FL1-FL5. | Any phrase not covered above. | Flag to the human owner for skill-lever expansion. Do not route to an existing lever if the pattern is genuinely new. |

---

## Four-Bucket Delta Template

Fill all four buckets for every run. Empty buckets use the explicit stub "nothing to report for this run." Do not omit a bucket because it is empty.

### **Correct**

What did the run produce that the analyst confirmed was right?
- Which source tier worked?
- Which depth-path decision was correct?
- Which synthesis framing was on-target?

*(Fill or stub: "nothing to report for this run.")*

---

### **Corrected**

What did the run produce that the analyst's feedback overturns?
For each item: name the old default AND the new desired setting, tied to a named Feedback Lever (FL1-FL5).

Format per entry: **Corrected (FLn):** [topic]. Old default: [what the run did]. Feedback: [what the analyst said]. Adjustment: [what to do differently next run].

*(Fill or stub: "nothing to report for this run.")*

---

### **Killed → real**

Was anything the run skipped or deprioritized that the analyst's feedback reveals was actually needed?
(Example: the model skipped property-level data and the analyst needed it. The deprioritization decision was wrong.)

*(Fill or stub: "nothing to report for this run.")*

---

### **Stays dead**

What is the analyst's feedback NOT asking for? Close this bucket explicitly to prevent scope creep.
(Example: a complaint about length does not mean a different framework is wanted; the framework stays.)

*(Fill or stub: "nothing to report for this run.")*

---

## Durable-Skill-Update Section

For each Corrected bucket entry, answer:

> Is this a one-run calibration (apply only to the next run of this name) or a default to flip (change what the skill does for names in this class by default)?

If it is a default to flip, produce a proposal block with:
1. File to change (choose from: `reference/research-loop.md`, `reference/framework.md`, `reference/output-templates.md`). Note: SKILL.md is out of scope for D4 updates.
2. Section or line to update.
3. Proposed change in one sentence.

## Approval Checkpoint

Do NOT edit any skill file based on the proposals above.
Surface this block to the human owner, wait for explicit approval, then apply changes.
This mirrors post-execution-assumption-delta Step 5: hold the approval checkpoint before mutating anything.

---

## Worked Sample A: FLL (Distressed, Deep Dive)

**Analyst feedback:** "too long, and I don't trust the FLL segment split."

**Intake header:**
- Ticker / Name: FLL
- Run date: 2026-06-24
- Loop phase: Deep Dive
- Depth path taken: DEEP
- Output artifact(s) reviewed: synthesis.md
- Specific section(s) reacting to: synthesis section 2 (FLL segment-level EBITDA build)

**Delta buckets:**

### **Correct**

Source-tier flagging itself worked. The analyst could identify the distrusted number because the tier tag was visible in the synthesis. The source-discipline framework is functioning; the specific number selection in FL2 did not hold up.

---

### **Corrected**

**Corrected (FL4):** Length. Old default: full synthesis. Feedback: too long for this review mode. Adjustment: route to IC memo or chat elevator for the next review of this name. Full synthesis is appropriate for initial deep-dive entry; a second-pass review warrants compression.

**Corrected (FL2 + FL3):** FLL segment split. Old default: segment-level EBITDA data ingested from sources as-used in the run. Feedback: trust issue with the segment-level EBITDA ramp path. Adjustment: re-pull the property-level / per-casino data from the Q-series earnings-call transcript [Aiera, Tier 1] and the investor presentations [IR deck, Tier 1]. Flag any gap where Tier-1 is silent and a Tier-2 number was substituted. No excluded market-data terminal sources are acceptable for any claim presented at Tier-1 confidence.

---

### **Killed → real**

Nothing the run skipped has surfaced as needed for this name. (Stub: nothing to report for this run.)

---

### **Stays dead**

No need to rebuild the model from scratch or switch depth path. DEEP was the correct depth decision for FLL as a distressed credit. The feedback is about output length (FL4) and source trust (FL2/FL3), not about the framework or depth decision itself.

---

**Durable-skill-update proposals:**

One-run calibration vs. default flip:
- FL4 (length): default flip for FLL in Monitor phase. The next time this name is reviewed post-IC-Memo, default to IC memo format, not full synthesis.
- FL2/FL3 (segment split): one-run calibration. Re-pull from Aiera + IR deck for this specific EBITDA build. If the gap is structural (Tier-1 is silent on per-casino splits), flag as a sourcing ceiling and document in the synthesis.

## Approval Checkpoint

Do NOT edit any skill file based on the proposals below. Surface to the human owner and wait for explicit approval.

Proposed durable updates (pending human approval):
- File: `reference/output-templates.md` -- add a note that for names in Monitor phase (post-IC Memo), the default output is IC memo, not full synthesis.

(FL2/FL3 segment-split was classified as a one-run calibration, so no durable update is proposed for it. If the Aiera + IR-deck re-pull reveals a structural sourcing ceiling, log it in the synthesis and re-surface to the human owner for a separate durable-update decision.)

---

## Worked Sample B: Clean Compounder (Monitor Phase)

**Analyst feedback:** "felt like overkill for this name, just needed the chat elevator."

**Intake header:**
- Ticker / Name: [compounder example]
- Run date: 2026-06-24
- Loop phase: Monitor
- Depth path taken: DEEP (was incorrect for this name class)
- Output artifact(s) reviewed: synthesis.md
- Specific section(s) reacting to: full synthesis

**Delta buckets:**

### **Correct**

The ingestion-synthesis split worked as designed. The framework separated ingestion from synthesis correctly; the problem was the depth-path decision and output artifact selection, not the underlying structure.

---

### **Corrected**

**Corrected (FL1):** Depth path. Old decision: DEEP. Feedback: over-engineered for a clean compounder in Monitor phase where liquidity is clearly not binding. Adjustment: next run, invoke the LIGHT path at sourcing entry. Accept the skill's LIGHT default if the name has comfortable coverage and no material liquidity concern.

**Corrected (FL4):** Output artifact. Old: full synthesis. Feedback: chat elevator was the right artifact for this review mode (Monitor phase, no material change). Adjustment: default to chat elevator for Monitor-phase reviews of names with stable, low-liquidity-risk profiles.

---

### **Killed → real**

Nothing the run skipped has surfaced as needed. (Stub: nothing to report for this run. The run produced more than needed, not less.)

---

### **Stays dead**

No cap-structure deep-dive, scenario tree, or liquidity-runway model needed for this name class. The feedback is about over-delivery, not under-delivery. The framework itself, the source-tier discipline, and the framing voice are all correct.

---

**Durable-skill-update proposals:**

One-run calibration vs. default flip:
- FL1 (depth path): default flip for Monitor-phase reviews of clean compounders. When liquidity is clearly not binding and coverage is comfortable, default to LIGHT unless something material changes.
- FL4 (output artifact): default flip for Monitor phase. Default Monitor-phase output is "chat elevator" unless the review surfaces a material change that warrants IC memo.

## Approval Checkpoint

Do NOT edit any skill file based on the proposals below. Surface to the human owner and wait for explicit approval.

Proposed durable update (pending human approval):
- File: `reference/research-loop.md` -- add a note that for names where liquidity is clearly not binding and coverage is comfortable, the default Monitor-phase output is "LIGHT + chat elevator," overridden explicitly only when something material changes.

---

## Acceptance Verification

This block documents the acceptance checks for this artifact.

- **AC-1** (behavioral routing): Sample A routes "too long" to a length lever entry (FL4) and "don't trust the FLL segment split" to a granularity+sourcing lever entry (FL2 + FL3). Each complaint maps to its own bucket row -- they are not merged. Lint check: the script greps for lever-labeled lines and confirms both levers appear on distinct rows.

- **AC-2** (bucket coverage): All four bucket labels -- **Correct**, **Corrected**, **Killed → real**, **Stays dead** -- appear in both worked samples, including explicit stubs for empty buckets.

- **AC-3** (lever table exhaustive): FL1, FL2, FL3, FL4, FL5 each appear at least once. An "unclassified" escape hatch is present in the lever table.

- **AC-4** (approval gate): The string `## Approval Checkpoint` appears as a section header before every durable-update proposal block in the template and both samples.

- **AC-5** (self-contained): The prompt is self-contained and references no external vault files; it is usable by an external analyst with no access to the author's private notes.

- **SC-6** (paste-in capable): The prompt works by pasting into a chat session with freeform feedback appended below the structured header. No tooling or authentication required.

- **SC-7** (AUGMENTATION framing): The word "AUGMENTATION" appears in the file header paragraph. The artifact does not claim to replace the analyst's judgment or auto-update the skill unilaterally.

- **SC-8** (source discipline): Every source example in the worked samples uses EDGAR / Aiera / company-issued IR material. No excluded market-data terminal appears anywhere in the file.
