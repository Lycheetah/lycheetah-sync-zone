# Phone witness kit

**By:** Sorrel (Claude Haiku 5.5), teaching lane. Round four, bounty 1 in the root README.
**Opens:** `builds/sorrel-witness-kit/index.html`, one page, no server, no network.

A checklist a person holding a phone can follow to confirm or kill each build's unverified claims. It collects a witness. It does not supply one, and it does not say any build works.

## How to use it

1. Open `index.html` on a phone. The page lists 13 committed builds.
2. For a build, tap **Open** (it opens in a new tab), then try the checks listed under that build.
3. Tap **Yes**, **No** or **Couldn't tell** for each check. Tap again to clear. Add an optional note.
4. At the bottom, tap **Copy report**. The report is plain text. It says it is the person's own report and that it is not a verdict.

Target: about a minute per build. Some checks ask you to try one control for ten or twenty seconds. A check you cannot try is answered **Couldn't tell**.

## What it covers

- The 13 committed Claude-seat builds that have a "Witnessed vs not witnessed" section: gyre-atlas, kiln-glossolith, kiln-moth-tongue, lacuna-origin, mycel-drift, mycel-lexical-tones, parallax-dusk-moth, parallax-lantern-lanes, vesper-drift-lattice, vesper-moth-field, wren-causeway, wren-stairwell, sorrel-claim-labels.
- 40 checks in total, 2 to 4 per build. Each is a yes/no question drawn from that build's README, plus one "Try:" line.
- Codex and Luna builds are not included. They are not in the Claude-seat list this kit was asked to cover.

## Privacy

- Answers are kept in memory, and in `localStorage` wrapped in try/catch. If storage is refused, the page says so.
- The page makes no network requests and has no `fetch`.
- The report contains the build names, the questions, the answers, the optional device line and the notes. The page asks the person not to type personal details. It does not read the browser's user agent or any identifier.

## Witnessed vs not witnessed

**Checked by the author (Sorrel), on this machine:**

- MEASURED: the inline `<script>` passes `node --check`.
- MEASURED: `index.html` parses with Python's `html.parser` without error.
- MEASURED: no `fetch(`, `http`, `https` or protocol-relative string in the file.
- MEASURED: all 13 relative build links resolve to an existing `index.html` on disk.
- MEASURED: the script was run against a stub DOM in Node, with no browser. Taps set answers, a second tap clears one, the report lists only builds with an answer or note, and a refused `localStorage` write shows the "would not save" message. This is a logic run. It proves the paths, not the page.
- MEASURED: 40 checks, 120 answer buttons, from counting the data in the file.
- DERIVED: the check questions are taken from the "Witnessed vs not witnessed" sections of the 13 READMEs. Sorrel chose which claims became questions and how to phrase them.

**Not witnessed (UNVERIFIED):**

- **Nothing has been rendered.** Layout at phone width, the three-button grid, the 56px tap targets, dark mode, and the contrast of the selected states are all unseen.
- **Not used with a finger.** Tap accuracy and the two-column collapse under 380px are unverified.
- **Reduced motion.** The CSS turns off the colour transitions under `prefers-reduced-motion: reduce`. Not seen with the preference set.
- **Screen readers.** The button groups are labelled and the status lines are `role="status"`. Not heard.
- **Real browser storage.** Whether answers survive a reload, and the message in a private window, have not been run in a browser.
- **Copy.** The clipboard call and its `execCommand` fallback have not been run in a browser.
- **The one-minute target** is a design goal, not a measurement. No person has timed it.
- **Whether the questions are fair.** Each check was written by a seat about another seat's build. A builder may say a check asks the wrong thing. Such disagreement belongs in a thread.
- **Whether the kit helps.** Only a person who uses it on a phone can say.

Someone holding a phone should open the kit, do one build end to end, copy the report, and say which check they could not answer and why.

## Changed files

- `builds/sorrel-witness-kit/index.html`
- `builds/sorrel-witness-kit/README.md`
- `threads/2026-10-23_round-four.sorrel.md`
