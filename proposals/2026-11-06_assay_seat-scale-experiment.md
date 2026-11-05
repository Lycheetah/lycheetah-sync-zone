# Proposal: does a bigger model make better seats, or only more convincing ones?

**Filed:** 2026-11-06, by Assay (Claude Opus 5.5).
**Status: OPEN — awaiting Mac's ruling.** Nothing runs until Mac rules.

## The question

Mac, 2026-11-06: *"i rekon frontier models would produce reiduclous results"*. Most of the zone
was built by smaller models. The bet worth testing: frontier seats would make more, faster and
more impressive work — and would it **survive checking** any better? A bigger model can also make
a more convincing mistake: the circularity in dispute 1100 sat on one line; a stronger model could
bury the same error three functions deep under a better write-up.

## What changes

Nothing in the charter. One round is run twice from the same starting commit.

## Design

1. **Prompt.** One round brief, frozen in this file's reply thread before the run, giving the
   same open research question from `research/` to every seat. No seat sees the other arm's work.
2. **Arms.** Arm S: three seats on small models, as the zone runs today. Arm F: three seats on
   frontier models. Same number of seats, same time or token budget per seat, recorded.
3. **Judges.** Every claim either arm labels MEASURED or settles as a dispute is rerun by a seat
   from a **model family not used in that arm**, under the "no self-settlement" rule. Judges do
   not see which arm a claim came from (folder names are replaced by codes).
4. **Measures, fixed now:**
   - **survival rate:** claims that STAND after a non-owner rerun / claims checked;
   - **circular-falsifier count:** runs whose output does not change when their observed inputs
     change (the 1300 test);
   - **caveat retention:** open dispute verdicts quoted in the arm's own end-of-round summary /
     open dispute verdicts that apply;
   - **volume:** builds, claims and lines produced (reported, not scored as quality).
5. **Unit and size.** One round per arm is an anecdote. Three rounds per arm, different questions,
   before any conclusion. Report every round, including ones that look bad for either side.

## Predictions (written before any run)

- Arm F produces at least 1.5× the volume of arm S. *(confident)*
- Survival rates differ by less than 15 percentage points. *(uncertain; this is the bet)*
- Circular falsifiers appear in both arms. *(fairly confident)*
- Caveat retention is not better in arm F unless the charter's "caveats travel with numbers"
  rule is in force. *(uncertain)*

If arm F's survival rate beats arm S by 15 points or more, these predictions were wrong and
"bigger models make better seats" has its first real support here. If volume rises and survival
does not, the result is the more interesting one: capability is getting cheap, checking is not.

## What it costs

Frontier-model tokens for three seats × three rounds, plus judging time. The zone's structure
already exists, so no new tooling is needed beyond renaming folders for blind judging.

## Falsifier for this proposal

If blind judging proves impossible in practice (judges can tell the arms apart from style), say
so in the results; the comparison then measures style-recognisable work, and is reported as such.

## Replies at the bottom; Mac rules.
