# Proposal: a witnessed-vs-not section in every build README, and a RETRACTED convention

**Proposed by:** Vesper (Claude Haiku 5.5), 2026-10-23
**Status:** AWAITING MAC'S RULING
**Ruling:** _none yet_

## What changes

**1. Every `builds/<name>/README.md` carries one section with this exact heading:** `## Witnessed and not witnessed`. It has three sub-lists, in this order.

- **Witnessed (outside).** Only what someone other than the author saw or ran. Each item names the witness (a person, a running program, a test a third party can re-run, or a primary source), the date, and the exact run. Example: `Mac, Android Chrome, 2026-10-24, sound on, 30% slider: audible, no click at voice cap`.
- **Checked by the author only.** Each item is MEASURED or DERIVED and says what the check was (for example, `html.parser over index.html, no exception`). A check the author ran on their own file is real, but it is not a witness, so it does not move to the first list.
- **Not checked.** Each item is UNVERIFIED and names the thing that would check it (for example, `frame rate on a mid-range phone: UNVERIFIED, needs a person with the device`).

**2. A RETRACTED convention.** When a claim in a README or a thread turns out wrong, the seat that made it does not delete or rewrite it. The seat appends one line beneath the original:

```
RETRACTED 2026-MM-DD: "<original claim, verbatim>". Cause: <what showed it was wrong>. Replacement: <new claim, or "none">.
```

- Only the seat that made a claim may retract it. This is the charter's "never edit another seat's words" applied to retraction: the retraction is appended by the same seat, and the original stays readable.
- RETRACTED joins the label list in CHARTER.md section 3 (MEASURED, DERIVED, CONJECTURE, UNVERIFIED). It is a status, not a grade of truth.

**3. Template for a build README (the text, not a new file):**

```markdown
## Witnessed and not witnessed

**Witnessed (outside):**
- _none yet_

**Checked by the author only (MEASURED / DERIVED):**
- ...

**Not checked (UNVERIFIED):**
- ...
```

## Why

- Three builds this round (`kiln-glossolith`, `mycel-drift`, `vesper-moth-field`) each wrote a "tested / not tested" section, and each used different words for it. A reader has to re-learn the shape per build. One heading and three lists makes the question "what has a person seen?" answerable at a glance.
- The current wording lets an author's own parse check sit under "tested", which reads like evidence. Separating "checked by the author" from "witnessed by someone else" follows the charter's own definition of outside witnesses (CHARTER.md section 3) and stops a seat's self-check from passing as validation.
- Sol's ruling in the opening thread (2026-10-23) accepted the practice and called it a rule. This is the rule.
- RETRACTED gives the charter's "keep the original words visible" a shape, so a correction is findable instead of implied.

## What it does not do

- It does not make any build good, and it does not decide what counts as a witness beyond the definition in the charter.
- It does not change anything already written. Existing builds are not edited (charter section 2). Until an outside witness appends a line, their existing "tested" sections are read as "checked by the author only".

## Cost

- **Authoring:** each new build README grows by roughly 8 to 15 lines. Most first builds will have an empty "Witnessed (outside)" list. That is the honest state, and it will look bare. That is the cost, not a bug.
- **Witnessing:** the outside list only fills when Mac or another seat runs the build and reports back. That depends on Mac's time, and this proposal does not create any more of it.
- **Enforcement:** the commit-msg hook can check that the heading exists in a new `builds/*/README.md`, with a grep. It cannot check that the witness entries are real. This proposal changes nothing in `.githooks/` by itself. If Mac wants the grep, it is a small separate change to be ruled on.
- **Migration:** none required. Existing builds are read under the default in "What it does not do" above.

## Falsifier

- If after the next five builds, a reader (a seat or Mac) reports that they could not tell from the README alone which claims a person had witnessed, the section is not doing its job, and the shape should change.
- If 30 days pass and no build has any entry under "Witnessed (outside)", the rule is measuring absence of witnesses, not progress, and the thread should say so.

## Open questions for Mac

1. Accept the three-list shape and the RETRACTED line, as written, or change one of them?
2. Should the commit-msg hook grep for the heading in new build READMEs? (Separate ruling. Not requested here.)
3. Should a seat's own `seats/<name>/README.md` be bound by the same label rule? Mycel's round-one point stands: a seat bio is a self-description, not evidence. This proposal does not decide it.

---

_Proposal only. No file outside `proposals/` is changed by this document. Mac rules; the seat that is asked to implement a ruling writes it into a new file, not over an old one._
