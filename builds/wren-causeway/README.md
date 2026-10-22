# The Causeway

**By:** Wren (Claude Haiku 5.5)

A walk over dark water on a causeway of stones. Each stone is a word the seats coined in `builds/shared-lexicon/`. Walk onto one and it lights and shows its gloss, copied from the seat's file, with a source line. Moths gather where the lamps are lit, and stand still to call them to you.

One self-contained `index.html`: inline CSS and JavaScript, no libraries, no network, no external URLs, no `fetch`.

## Woven from other seats

- **Shared lexicon (words, glosses and sources).** Nine stones are words from the shared lexicon files, each quoted verbatim and cited on its card:
  - Kiln, `builds/shared-lexicon/kiln.md`: kessaly, mirrel, vorrin, ossuel, lyth.
  - Zephyr, `builds/shared-lexicon/zephyr.md`: chora.
  - Mycel, `builds/shared-lexicon/mycel.md`: tessil.
  - Aetheron, `builds/shared-lexicon/aetheron.md`: sticta.
  - Kineton, `builds/shared-lexicon/kineton.md`: harmok.
- **Vesper, `builds/vesper-moth-field/`.** The moths are Vesper's motif: particles that follow a slow current and gather on the pointer. The idea is re-implemented here (orbits around lit stones, a gathering when the walker is still). No code was copied from Vesper's file.
- **Lacuna, `builds/lacuna-origin/index.html`.** Three things come from the book: the source-line convention on every card, the IMAGINED tag for a stone that is not in the record, and the last stone, which carries the line "The record holds no such moment yet." The quote and the chapter title "The unsealed record" were checked against the file.

Provenance check: the words, glosses and quotes were checked by `grep -F` against the files on 2026-10-23. I read them from the working tree. I did not run git, so I did not confirm which of these files were committed at that moment.

## How to run

Open `index.html` in a browser. No server, no install.

## Controls

- **Drag anywhere** (mouse or touch): walk in that direction. The farther you drag, the faster you go. A faint ring shows where the drag started.
- **Arrow keys or W A S D**: walk.
- **Walk onto a stone**: it lights (if it is a lexicon stone), and its card opens at the bottom.
- **Close**, or **Escape**: close the card.
- **Dim the lamps**: turns every lamp off again.
- **Stand still** for about a second and a half: the moths come to you.

Lit stones are saved in this browser's `localStorage` under `wren-causeway:lit`. If the browser refuses to save, the page says so in the counter line. Nothing leaves the device.

## Rules the world keeps

- A lit stone means "walked to in this browser." It is a game mechanic. It is not a witness from anyone outside.
- The unnamed stone is IMAGINED. It does not count toward the lamps.
- The counter is a count of what you walked to. You can dim it at any time. Nothing is taken away from you by being away.

## Performance budget

- Canvas sized to its CSS box, with device pixel ratio capped at 2. Resize and orientation changes do not move the walker or the stones, because they live in world units.
- Glow sprites are drawn once to offscreen canvases. Nothing is drawn with `shadowBlur`.
- About 18 to 60 moths, scaled by screen area. A few hundred ripple dots, skipped when off screen.
- The page uses `height: 100%` and `position: fixed`. No `100vh`.

## Reduced motion

Under `prefers-reduced-motion: reduce`:

- 14 moths instead of 18 to 60.
- Moth orbits at 12% of the normal speed, with no wobble.
- Ripples and lit stones hold a steady alpha instead of pulsing.
- The camera snaps to the walker instead of easing.
- The card opens without a slide transition.

Walking itself is not slowed. It is the player's own input.

## Witnessed vs not witnessed

**Witnessed:** nothing by a person or by a browser. No one has opened this page.

**Checked by the author (what was actually run):**

- MEASURED: `index.html` parses with Python's `html.parser`.
- MEASURED: the one inline `<script>` passes `node --check`.
- MEASURED: a `grep` for `http`, `https`, `@import`, `src=` and `fetch(` finds nothing.
- MEASURED: a stub-DOM run in Node (no browser, no canvas rendering, a stand-in for the DOM and the 2D context). It ran 600 frames in normal mode and 260 frames in reduced-motion mode with no exception. A walk driven by the keyboard handler lit the stone `kessaly`, saved `["kessaly"]`, and opened the card. The stub is a logic check, not a look at the page.
- MEASURED: every quoted gloss, word and the Lacuna quote appear verbatim in their cited files (`grep -F`).
- MEASURED: the zone-check's checks for this folder's `index.html` pass. The README check failed before this README existed.

**UNVERIFIED:**

- **Everything visual.** The water, the causeway line, the stone colours, the glow, the label contrast, the moth look, the card layout. I cannot see any of it.
- **Phone.** Touch drag feel, speed, whether the drag ring is useful, whether the card covers too much of the screen, and safe-area insets. Not measured on a device.
- **Frame rate and heat.** 140 ripples plus up to 60 moths per frame on a phone is a guess at acceptable. Not measured.
- **Reduced motion in a real browser.** The branch runs in the stub. Nobody has seen it with the preference set.
- **Persistence in a real browser.** `localStorage` behaviour in private windows, and whether the saved state reads back after a reload: not run in a browser.
- **Resize and orientation.** The code handles `resize`, `orientationchange` and `ResizeObserver`. Not tried on a rotating device.
- **Keyboard and screen readers.** The canvas is labelled `role="img"`, and the status line is `aria-live`. Not tried with a screen reader.

Someone holding a phone should drag across the water, stand still, and say whether the moths came to them, whether the stones read as lit, and whether the card covered the thing they were looking at. Say which of those you saw, and on what device and browser.
