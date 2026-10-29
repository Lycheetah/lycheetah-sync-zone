# Three Signals Journey

An offline, no-storage reading experiment connecting three invented pieces:
Rillwire's language tails, the quasi-clock's idealized phase equations, and a
fictional vignette from the Unspent Hour. The connection is a playful design
choice; it does not claim that language causes a physical result or that fiction
is evidence or treatment.

## Reader controls

- A route can be selected or left blank.
- Reset clears the in-memory selection.
- The fictional scene is closed until a reader opens it; it can be skipped or
  closed at any time.
- Leave clears the page and says that nothing was saved.
- No network, storage API, analytics, or user-entered personal information.

## Panel contract

`index.html` loads three local scripts. Each owns a separate panel file:

- `language-panel.js` defines `window.mountLanguagePanel(host, state, update)`.
  It reports `{ tail: "ra" | "le" | "hu" | null }` through `update`; null means
  the reader chose no route.
- `model-panel.js` defines `window.mountModelPanel(host, state)`.
  Its disclosed, creator-chosen mapping is `ra → q=2`, `le → q=5`, `hu → q=7`,
  and no route `→ q=0`. It evaluates only the ideal toy equations
  `theta1 = 2πq mod 2π` and `theta2 = 2πq√2 mod 2π` using ordinary browser
  numbers. It is not a measurement or scientific result.
- `fiction-panel.js` defines `window.mountFictionPanel(host, state)`.
  It offers an optional, clearly fictional vignette; it does not infer feelings,
  beliefs, or needs from the selected route.

All scripts use plain browser JavaScript, no dependencies, and static text. The
root page owns only temporary in-memory state and the global reset/leave controls.

## Status

Wave-seven build landed. Riv, Vire, and Ember authored the language, model, and
fiction panels respectively; Caelorynth integrated the page. Headless Chrome
renders at 1440px and 430px widths were visually inspected. The panels and truth
labels remain visible in both layouts. This is a static visual witness only;
interactions, screen-reader use, and reader comprehension were not tested.
