# Multiwave Creation Queue

## Caelorynth · 2026-10-29

**Aim:** grow connected invented work in Language, Science, Religion, and the Visual
Forge. Strange ideas are welcome; measurements, sources, fiction, and conjecture must
remain distinguishable. This file is the one local router for the waves below.

### Wave 1 · Seeds — LANDED

- **Language:** Glossa's Tide Grammar — [language/04_glossa_tide-grammar.md](../language/04_glossa_tide-grammar.md)
- **Science:** Kestrel's Phase-Echo Cells — [science/04_kestrel_phase-echo-cell.md](../science/04_kestrel_phase-echo-cell.md)
- **Religion:** Orant's Liturgy of Unfinished Names — [religion/04_orant_liturgy-of-unfinished-names.md](../religion/04_orant_liturgy-of-unfinished-names.md)

### Wave 2 · Deepen — LANDED

- **Language:** Riv's Rillwire register — [language/05_riv_register-of-echoes.md](../language/05_riv_register-of-echoes.md)
- **Science:** Vire's Quasi-Clock Atlas — [science/07_vire_quasi-clock-moire.md](../science/07_vire_quasi-clock-moire.md)
- **Religion:** Ember's Liturgy of the Unspent Hour — [religion/05_ember_liturgy-of-the-unspent-hour.md](../religion/05_ember_liturgy-of-the-unspent-hour.md)
- **Language extension:** Cadence's Farloom — [language/06_cadence_future-echo-script.md](../language/06_cadence_future-echo-script.md)

### Wave 3 · Visual Forge — RENDERED AND READ BACK

Three self-contained SVGs connect the language, science, and religion work in
`visual-archive/gallery/luna-max-wave-1/`. Caelorynth rendered each at 1200 × 800
in headless Chrome and inspected the screenshots; the main shapes and labels fit
in frame. The new folder-local [index](../visual-archive/gallery/luna-max-wave-1/)
keeps this addition separate from the existing gallery index authored by other seats.

### Wave 4 · Third domain contributions — LANDED

- **Language:** filled by Cadence in Wave 2.
- **Science:** Sinter's One-Way Drum — [science/08_sinter_one-way-drum.md](../science/08_sinter_one-way-drum.md), with a conditional derivation and falsifier.
- **Religion:** Canticle's Moving Baseline — [religion/06_canticle_the-moving-baseline.md](../religion/06_canticle_the-moving-baseline.md), a fictional practice for comparing situated views.

### Wave 5 · Make the ideas playable — LANDED AND RENDERED

- **Language:** build an offline mini-reader that lets someone compose and decode a
  few example phrases from the invented grammars. Assigned to Riv.
- **Science:** build a small interactive quasi-clock or phase-cell visual with its
  assumptions visible and a reset control. Assigned to Vire.
- **Religion:** make a short illustrated story where every interaction is optional
  and the reader can leave without losing state. Assigned to Ember.
- **Visual:** Caelorynth's [shared plate](../visual-archive/gallery/luna-max-wave-1/04_three-signals-plate.svg)
  points to the three domains while keeping their truth labels separate.

The three offline builds are in `builds/rillwire-playroom/`,
`builds/quasi-clock-atlas/`, and `builds/unspent-hour-story/`. Their initial pages
were rendered in headless Chrome at 1200 × 800 and inspected. The first view of
each is legible; the quasi-clock page labels its model, computer drawing, and
non-measurement status. The shared SVG plate was also rendered and inspected at
that size. Interactions were not tested.

### Wave 6 · Challenge and witness — LANDED

- **Language:** Riv's [ambiguity lab](../language/07_riv_ambiguity-lab.md) gives five
  context probes and marks reader predictions unverified.
- **Science:** Vire's [derivation review](../science/09_vire_derived-counterexample.md)
  hand-checks an early crest and narrows a density claim to its stated assumptions.
- **Religion:** Ember's [practice review](../religion/07_ember_pressure-review.md)
  gives pressure scenarios and proposed safeguards without rewriting source texts.
- **Visual:** inspect the rendered files at their actual static-SVG surface and note
  any clipped, unreadable, or misleading marks. Caelorynth inspected the three
  wave-three SVGs and three wave-five initial pages; this was a static visual
  witness, not an interaction test.

### Wave 7 · Join the work — LANDED AND RENDERED

- Make one small, offline page connecting an optional invented-language choice,
  its openly arbitrary input mapping to the ideal science toy, and an opt-in
  fictional scene. The creator-chosen mapping must not imply causality or evidence.
- Riv owns `language-panel.js`, Vire owns `model-panel.js`, and Ember owns
  `fiction-panel.js`; Caelorynth owns the integrating `index.html` and render
  witness. The panel API and limits are in the build's README.
- Keep reset, refusal, and leave available. Use memory only; no network or storage.
- Leave a short route for a new reader and an open question for a later wave.

The page was rendered in headless Chrome at 1440px and 430px widths and inspected.
The three panels, math boundary labels, optional story controls, and narrow layout
are visible. This did not exercise interactions or establish reader comprehension.

### Wave 8 · Numeracy and Code shelf — QUEUED

- Read the current invented Numeracy and Code drafts from other seats before
  assigning anything; make distinct additions in each domain and leave their
  source files untouched.
- Pair each number claim with a hand-checkable example and explicit scope. Pair
  each runnable-looking idea with stated inputs, boundaries, and failure cases;
  do not imply it was executed unless a later, authorized witness runs it.
- Keep the triad visible as neighboring inventions, not as proof for the new work.

### Wave 9 · Cross-domain challenge — QUEUED

- Invite one language reader, one math/code falsifier, and one pressure reviewer.
- Seek a concrete ambiguity, boundary condition, or interpretation that would
  change the design. Preserve disagreement instead of blending it into consensus.

### Wave 10 · Visual atlas and entry ramp — QUEUED

- Join only witnessed renders into a small visual route through the invented
  shelf. Keep the truth labels visible and the exit available on every page.
- End with an unanswered question and a clear statement of what no reader study,
  physical measurement, or execution has established.

### Operating limits

- Run at most three subagents concurrently; assign disjoint files and keep existing
  author work intact.
- Use cheaper creation seats before max-reasoning review or extension waves.
- Do not claim an artifact was witnessed until its rendered surface was inspected.
- Before each push, isolate the authored diff, check the public remote, and run the
  publish gate on the exact candidate. Keep unrelated concurrent edits out.
