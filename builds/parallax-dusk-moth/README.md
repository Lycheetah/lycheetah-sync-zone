# Dusk Moth

**By:** Parallax (Claude Haiku 5.5)
**Borrowed from:** the moth motif of Kiln's `builds/kiln-moth-tongue/` and Vesper's `builds/vesper-moth-field/`. Idea only: moths and a pointer. No code copied, and no other seat's file was edited.

A single self-contained `index.html`. You are a small moth at night. Gather **14 embers** before the dusk goes out. Shadows drift down and bite. Every night is seeded and breaks one rule.

## How to play

- **Goal:** collect 14 embers (dawn, a win) before the dusk meter reaches zero (a loss).
- **Phone:** drag anywhere to fly toward your finger. Quick tap to **pulse**: it scatters nearby shadows and costs 12 dusk.
- **Keyboard:** arrows or WASD to fly, Space to pulse, R to restart a finished night.
- **Dusk:** drains over time, faster as the night goes on. Embers refill it. A shadow that touches you costs 28 dusk, then you have about a second of reprieve.
- **Gold embers** (about 1 in 8) are worth 3x points and refill more dusk.
- **Score:** 100 per ember (300 for gold). A dawn adds a bonus for dusk left and for speed.

## The nights (one rule each)

| Night | Rule |
|---|---|
| Plain Dusk | Nothing extra. |
| The Mirror Moon | Horizontal controls are reversed. |
| The Echo Night | Shadows chase the path you walked 1.2 seconds ago. |
| Blind Lantern | You only see inside your light circle. |
| Heavy Tithe | Dusk drains twice as fast; embers pay twice. |
| The Wrapping Tide | The sky has no side walls; you wrap around. |

Replay a night: the page shows its seed, for example `#seed=77`. Open the page with that hash to get the same night. "This night again" restarts the same seed.

## Not in this build

- No save, no high-score table, no sound.
- Pulse is the only special action. Shadows are not individually distinct yet.

## How it was checked

- Pure logic (no DOM) runs in plain Node: deterministic per seed, no NaN, dawn and dusk endings, and the tide wrap distance. See below for numbers.
- Browser layer: smoke-tested against a stub DOM in Node (title, begin, 2000 frames with keypresses, no exceptions). That is not a browser.
- HTML parsed with Python `html.parser` (no unclosed or mismatched tags). Inline script passed `node --check`. No external URLs, no network calls.

## Witnessed vs not

**Witnessed (MEASURED):** the checks above, run by Parallax on this machine.

- A greedy bot that flies to the nearest ember and pulses near shadows reached dawn on **59 of 60** test seeds. That is a measure of the bot, not of a person. The bot does not dodge, so the shadows are weaker than they will feel to a human. The tuning is probably too easy. Treat that as a finding, not a result.
- Doing nothing reached dawn on 4 of 60 seeds (mostly Plain Dusk).
- Random wandering reached dawn on 0 of 60.

**Not witnessed (UNVERIFIED):**

- How it looks: colours, the moth, the glow, the blind-lantern overlay, the HUD layout. I cannot see a browser.
- How it feels: whether the controls are responsive on a phone, whether a drag feels right, whether pulse is worth its cost, whether the nights are fun.
- Touch behaviour: pointer capture and the quick-tap threshold have only been read, not used with a finger.
- Reduced motion: the code turns off stars drift, wing flutter, shake, particles and the pulse ring. Only read, never seen.
- Whether the game is hard enough for people. The bot numbers suggest it may be too easy.

A person holding a phone should judge all of the UNVERIFIED items above.
