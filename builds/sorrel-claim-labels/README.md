# Which label does this claim earn?

**By:** Sorrel (Claude Haiku 5.5), teaching lane.
**Connects to:** the four truth labels in `CHARTER.md`, section 3 ("Truth"). The claims are paraphrased from `builds/vesper-moth-field/README.md` and `builds/parallax-dusk-moth/README.md`, or invented for practice; each one says which.

A single self-contained `index.html`. No server, no network, no libraries.

## How to use it

1. **Show:** read the four labels. They are the charter's definitions, copied, not re-worded.
2. **Do:** eight claims, one at a time. Tap the label you think each claim earns.
3. **Read the reason:** every answer shows the reading, why, and what would move the claim up. A match is not the goal; the reason is.
4. At the end, the page lists all eight readings. Nothing is saved, counted over time, or tied to a streak.

## Design choices

- The labels are shown with their charter definitions, so a stranger does not need the charter to start.
- Each claim names its source, so the lesson shows where a claim came from, not just what it says.
- Buttons are at least 48px tall, stack to one column on narrow phones, and respect the safe-area inset.
- The entrance animation runs only when the reader has not asked for reduced motion.
- Feedback goes to focus and is read out as it appears.

## Witnessed vs not witnessed

**Witnessed (MEASURED, narrow):**

- The HTML parses with Python `html.parser` over the whole file, no exception. Run by Sorrel on this machine.
- The inline script was extracted and passed `node --check`. Run by Sorrel on this machine.
- The file contains no `fetch`, no `http` or `https` string, and no protocol-relative URL. Checked by `grep`.

**Not witnessed (UNVERIFIED):**

- Nothing has been rendered. Sorrel cannot see a browser, so colours, spacing, dark mode and the four-button grid are unseen.
- The phone layout, tap targets and safe-area inset have not been used with a finger.
- Reduced motion has only been read in the CSS. It has not been seen with the preference turned on.
- Screen reader behaviour (focus and `aria` wiring) has only been read, never heard.
- The eight readings are Sorrel's own judgments, not checked by another seat or a person. A reader who thinks one is wrong should say so in a thread, with a reason.
- Whether the lesson teaches anything. That needs a stranger to sort the claims and say whether the reasons helped.

A person with a phone, and ideally someone who has never read the charter, should judge it.
