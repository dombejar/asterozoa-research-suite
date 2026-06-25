# Output Templates

Three artifacts. The investment-angle synthesis is the most important output: a committed analytical view on the security (mispriced or not, which instrument best expresses the view, what evidence would flip the read). The IC memo is the canonical decision document. The chat elevator is what actually gets read. Voice constraint applies throughout: no em dashes, plain language, no AI-hedge phrases, no consulting-speak.

A note on source tiers in every artifact: the source flags from the ingestion pass travel forward. When a synthesis point, a memo claim, or an elevator line leans on a fact, the underlying source tier is attached, so a bull point resting on a Tier-3 web fact is visibly weaker than one resting on a 10-K.

---

## Output-length mode dispatch

Pass `--mode <value>` to select the rendering at the end of PASS 3. Default is `full`. Mode controls rendering only, not ingestion depth: all three passes run in full regardless of mode.

### Modes

**`bullet`** (default: `--mode full`; use `--mode bullet` for chat-ready summary):
Preserves the Artifact C (chat elevator) content shape: analytical stance, thesis, variant view, why now, instrument read, exit triggers. Renders as a block of plain lines with no markdown section headers (no `#`, `##`, `###`). Inline field labels (`Thesis:`, `Variant view:`, `Why now:`, `Instrument:`, `Exit triggers:`) are allowed as line-opening prefixes; they are labels, not headers. Line 1 must be a substantive key-insight sentence (not a label or a header). Budget: 6-10 lines, approximately 200 words maximum. This is the Artifact C content structure with a slightly looser line budget (Artifact C specifies 6-8 lines; bullet mode allows up to 10 for edge cases). The `Memo:` line from Artifact C is intentionally omitted in bullet mode: bullet mode is a standalone chat-ready summary that does not presuppose an attached memo. When the full IC memo is available and the reader needs a link to it, use `--mode full` instead.

**`exec-summary`** (use `--mode exec-summary` for condensed IC output):
A condensed format collapsing Artifacts A and B into approximately 2-3 pages. **Key Insights must be the first rendered content** (hard rule: Key Insights leads, no introductory prose before it). After Key Insights: condensed thesis, variant view, key risks, and valuation summary. Budget: 600 words maximum.

**`full`** (default):
Renders all three artifacts: Artifact A (investment-angle synthesis), Artifact B (IC memo), and Artifact C (chat elevator). No length cap.

### Length budget table

| mode | budget |
|------|--------|
| `bullet` | `<= 10 lines / ~200 words` |
| `exec-summary` | `<= 600 words` |
| `full` | no cap |

### Key Insights first-line contract (hard rule for exec-summary)

In `exec-summary` mode, the Key Insights block is the first rendered content. No introductory paragraph, no business-overview preamble, no transition prose before it. The reader sees Key Insights first. This is not a recommendation: it is a structural requirement of the exec-summary format.

### Defaults

`--mode full` by default (preserves existing behavior; all three artifacts rendered). `--mode bullet` targets Artifact C content shape (6-10 lines, approximately 200 words, substantive key insight as line 1).

---

## Artifact A: The investment-angle synthesis

This is the most important output and the explicit reason the skill exists. It runs as PASS 3, AFTER ingestion completes, as a distinct pass reasoning over the source-tiered base. The ingestion pass produced BACKGROUND. This pass produces a VIEW.

The view is analytical: is the security mispriced (and which way), which instrument best expresses the view (equity vs a specific debt instrument), and what specific evidence would change the read. The "no hedge-everything" discipline holds: commit to a view on the security, state it plainly, and name the falsifying data point. The skill does not declare an allocation decision; the reader makes that call.

It anchors its bull/bear on the cash-generative reality (because the model already bridged EBITDA to cash) and treats management's adjusted-EBITDA framing as the thing to pressure-test, not accept. It is micro-first; a macro section appears only when an assumption depends on it.

```
# {TICKER} Investment-Angle Synthesis

Depth path: [DEEP / LIGHT] because [liquidity-binding signal, or steady-grower rationale].

## 1. Bull case
Why the security screens interesting on the long side. The affirmative thesis,
grounded in the ingestion facts, with source tiers attached. Anchored on cash
generation, not the adjusted-EBITDA story. Where applicable, state the franchise
test: does EPV exceed asset value, and what is the moat that holds the gap open.

## 2. Bear case
The symmetric downside thesis. What breaks it. Specific and operational, not
"multiple compression" or "macro." Name the metric, the competitor, the
covenant, or the maturity that does the breaking.

## 3. Why it is interesting / why now
The catalyst and the reason this name rises above a screen. State explicitly
what makes it worth concentrating attention on right now, not a neutral profile.
(FLL shape: a binary catalyst, the combined refi-with-cash-out event, plus an
EBITDA ramp, inside a short catalyst window.)

## 4. Variant view / where do you most see the model break
The restructuring-trained instinct: find the point of maximum fragility. Name
where the consensus or the base-case assumption is most likely wrong, and the
single data point that would flip the thesis. Not just "here is the base case"
but "here is the break point and here is the data that would invalidate it."

## 5. Key risks (ranked by materiality, tied to assumptions)
Enumerated and ranked. Each risk maps to the specific model assumption it would
break. (FLL examples: temporary-license expiry, financing/refi overhang, the
property ramp running behind plan.)

## 6. Instrument read
Which security is the right expression of the view, and why: equity vs a
specific debt instrument (note, term loan, revolver, fulcrum security).
If no public debt exists, state that plainly.

## [Distressed module, DEEP path only]
- Liquidity-runway estimate (FTI 13-week-style, weeks until cash depletes).
- Strategic-alternatives scenario set (keep-extending / new-debt / refi /
  refi-with-cash-out / sale-leaseback), each off the one assumption block.
- Recovery-by-seniority (where value breaks in the cap stack, who holds the
  fulcrum security).
```

---

## Artifact B: The IC memo (canonical structure)

The compressed argument, 3-8 pages, for a senior reader with 15 minutes. The deep dive working file holds the 20-50 pages; the memo is the extract. Front-load: most IC decisions are made on the first two pages (recommendation, thesis, variant view, risks). Sources for the canonical structure: [Daloopa hedge fund investment memo example](https://daloopa.com/blog/analyst-best-practices/hedge-fund-investment-memo-example), [Stanford Addepar investment memos and decision-making](https://longterminvesting.stanford.edu/sites/g/files/sbiybj23856/files/media/file/addepar-investment-memos-and-decision-making.pdf), [Wall Street Oasis stock pitch template](https://www.wallstreetoasis.com/resources/templates/word-templates/stock-pitch-sample-template).

```
1. ANALYTICAL STANCE (one paragraph)
   Long / short / pass / watch on the security. The analytical view in plain
   English: mispriced or not, and which way. Which instrument best expresses
   the view. Time horizon for the thesis. Target with base / bull / bear.
   Catalysts in window. The reader decides on allocation; the memo provides
   the view.

2. THESIS (three sentences max)
   Sentence 1: business in plain English.
   Sentence 2: what the market believes vs what we believe.
   Sentence 3: why the gap closes within the time horizon.

3. BUSINESS OVERVIEW (1 page)
   What they sell, to whom, in what unit economics. Segment mix and economics.
   Where value comes from at the unit level. Source-tagged from the 10-K and
   the transcript/IR-deck granular pull.

4. VARIANT VIEW (1 page, load-bearing)
   Consensus paragraph (sell-side, implied multiples). Our view paragraph
   (specific operational claims with numbers). Why we are right paragraph.
   Name a specific number, not a vibe.

5. CATALYSTS (half page)
   Named catalysts with windows. What each tells us if it lands, and if it slips.

6. VALUATION (1 page)
   The abbreviated model's exit chain: multiple-on-EBITDA to EV to minus-debt
   to equity value to price per share, every EBITDA figure paired with its
   cash-from-ops bridge. Base / bull / bear scenarios off the one assumption
   block. Triangulate with the comps table. State the margin of safety.

7. RISKS AND MITIGANTS (half page, required)
   Specific operational risks, named. Probability and impact. Mitigants in our
   control (sizing, exit triggers) and out of our control (recovery scenarios).

8. POSITION SIZING (half page)
   Initial position, pyramid plan (add at what price tiers), max position, and
   why this size and not bigger or smaller.

9. EXIT TRIGGERS (half page, decays well)
   Thesis-broken triggers (operational, named, not price targets). Thesis-
   confirmed re-rate triggers. Re-underwrite events. Write these at memo time.

10. APPENDIX (variable)
    The abbreviated one-tab model, peer comp, source list (with tiers), open
    questions. On the DEEP path, the liquidity-runway and recovery waterfall.
```

What separates great memos: the thesis fits in three sentences; the variant view names a specific number; risks are operational not categorical; exit triggers are pre-committed; sizing is justified; length stays 3-8 pages.

---

## Artifact C: The chat elevator (what actually gets read)

6-8 lines, dropped into team chat, in your own voice. The memo is the supporting document only a senior reader opens with a question. Voice: no greeting filler, plain language, no AI hedges, no em dashes.

```
{NAME}: [long / short / pass / watch] on the security

Thesis: [one sentence on the business, one on the analytical view, one on the catalyst].

Variant view: [one paragraph naming the specific operational claim and the numbers].

Why now: [one sentence on the catalyst window].

Instrument: [which security is the right expression: equity / specific debt instrument].

Exit triggers: [one bullet thesis-broken trigger, one confirmation trigger].

Memo: [link or attached].
```

---

## Which artifact for which reader

| Artifact | Reader | Length | When |
|----------|--------|--------|------|
| Investment-angle synthesis | The analyst + IC | 1-2 pages | After ingestion + model, every name that advances |
| IC memo | The investment committee | 3-8 pages | Per initiation |
| Chat elevator | Team chat | 6-8 lines | Per memo, the thing that actually gets read |

Default question before producing anything: who is going to read this and what decision are they making? Match the audience.

---

## FLL Worked Sample

Full House Resorts (FLL) is the recurring worked example across the skill. Three mode renderings below, all FLL-specific.

**NOTE: all figures and claims in this section are illustrative placeholders that show output shape and format. They are not sourced from live filings, Bloomberg, or any canonical data pull. Do not treat any number here as a verified fact. A real research output must source-tag every factual claim per the source-tier taxonomy and inline tag convention defined in `reference/research-loop.md` (the `## The source-tier taxonomy` section).**

### bullet mode rendering (--mode bullet)

FLL: analytical read favors the equity as the cleaner expression; binary catalyst in a short window makes the setup worth concentrating attention on now.
Thesis: FLL owns its real estate and is executing a refi-with-cash-out that, if it clears, funds the EBITDA ramp the market is not pricing; the market sees the 8.25% 2028 note overhang as a blocker, the analysis reads it as the entry point.
Variant view: consensus is treating the temporary gaming-license renewal as a routine formality; a delay past Q3 pushes the refinancing window and compresses the equity cushion by 15-20 points.
Why now: the refi window opens in Q2 and closes by Q4 as the call protection steps down; the EBITDA ramp at the two new properties accelerates through the same window.
Instrument: equity only (the 8.25% 2028 notes are not callable at par until Q2; the equity is the better-risk-adjusted expression of the refi-with-cash-out thesis).
Exit triggers: license delay past Q3 (thesis broken); refi clears and 12-month forward EBITDA in line with ramp plan (confirmation re-rate).

### exec-summary rendering (--mode exec-summary)

**Key Insights**
- FLL owns its real estate outright; the 8.25% 2028 note overhang is the entry point, not the blocker, because a refi-with-cash-out funds the capex ramp without diluting the equity cushion.
- The market is mispricing the gaming-license risk as binary; it is actually a timing risk that compresses the refi window to a 6-month band in 2026.
- If the license clears by Q3 and the refi is in market by Q4, the EBITDA trajectory at the two new properties gives a 2.5-3x return on a 12-month horizon at current entry.

**Thesis**
FLL operates a portfolio of owned gaming properties with a concentrated near-term catalyst: refinance the 8.25% 2028 senior notes with a cash-out component, fund the two-property EBITDA ramp (projected +$45M EBITDA over 24 months from Phase 2 completions), and close the current 6-7x EV/EBITDA discount to peers at 9-10x. The market believes the temporary gaming-license renewal is a material binary risk; we believe it is a timing risk that shifts the refi 1-2 quarters, not a thesis-breaker, because the notes are callable beginning Q2 2026 and the step-down schedule gives a 6-month optimal execution window.

**Variant view**
Consensus assigns a 70-80% probability to smooth license renewal and is pricing FLL at a 6.2x NTM EBITDA multiple versus peers at 9.1x. Our view: the discount is rational if the license delays into Q4 but is excessive by 200-250 basis points if license clears by Q3 and the refi executes inside the call-step window. The specific number that would flip the thesis: a license-delay notice past August 15 that pushes the refi into 2027 and forces a covenant amendment on the 2028 notes.

**Key risks (ranked)**
1. License delay past Q3 2026: compresses the refi window, triggers covenant headroom review, and removes the why-now from the thesis. Probability: 25%. Impact: thesis broken, exit.
2. EBITDA ramp behind plan at Phase 2 properties: reduces the cash-out quantum available in the refi and narrows the equity cushion. Probability: 35%. Impact: reduces position to 1.5%, re-underwrite at Q2 results.
3. Rate environment widens HY spreads 150bp: the refi cost rises and the accretion math on the cash-out deteriorates. Impact: model sensitivity on cash-from-ops post-refi; monitor, not exit trigger.

**Valuation**
Base case: refi clears Q3, EBITDA ramp on plan, 8.5x NTM EBITDA exit multiple, equity value per share $28-32. Bear case: license delay to Q1 2027, EBITDA flat, 6.5x multiple, equity value $14-16. Bull: license Q2, ramp 10% ahead of plan, 9.5x multiple, $38-42. Current entry: $18.50. Margin of safety in base case: 52-73%.

### full mode

Full mode renders all three artifacts (Artifact A investment-angle synthesis, Artifact B IC memo, Artifact C chat elevator) per the templates above. For FLL: PASS 3 synthesis uses the refi-with-cash-out event as the spine of the bull case, the temporary-license timing risk as the variant view, and the 6-month call-protection step-down as the why-now anchor. No additional worked text is reproduced here; the canonical FLL full-mode output lives in the per-company folder.
