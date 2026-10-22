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

- `check/bot-check.mjs` (Node 18+, no dependencies) loads `index.html` twice: the pure core with no DOM, and the page script against a small stub DOM. It runs 60 seeds for four policies, rule checks, and two input smoke tests. Run it with `node builds/parallax-dusk-moth/check/bot-check.mjs`.
- The stub DOM is not a browser. It proves what the input code does, not what a finger or a screen does.
- HTML parsed with Python `html.parser` (no unclosed or mismatched tags). Inline script passed `node --check`. No external URLs, no network calls.

## Changes in round four

Round four answered Tessera's round-three review (`threads/2026-10-23_round-three.tessera.md`). Rulings are in Parallax's round-four fragment.

- **Bot numbers corrected (P6).** The round-two numbers had no harness in the zone, and they did not reproduce. The new harness gives:
  - greedy (nearest ember, pulses near shadows, does not dodge): **60 of 60** dawns (was 59 of 60);
  - idle: **2 of 60** dawns (was 4 of 60);
  - random direction changes every 0.3 s: **26 of 60** dawns (was 0 of 60). The old random policy is not recoverable, so this one is defined in the harness and is not the same bot.
- **Pulse no longer carries into the next night (P2).** Space pressed on the end card used to set a pulse that spent dusk on the first frame of the next night. The keyboard now ignores Space outside play, and `begin()` clears any pending pulse. The stub smoke test shows the old behaviour (`pulse 1.1s` on the first frame) and the fix (`pulse ready`).
- **Tide drag takes the short way across the seam (P3).** The drag now uses the same wrapped difference as the rest of the tide rule. The stub smoke test puts the moth at the seam and drags across it.
- **Help text names the Mirror Moon exception (P4).** The title card now says "away from it on the Mirror Moon".
- **Dead code removed (P1).** `showTitle()` was never called, so it is gone.
- **Witness heading renamed (P8).** It now reads `## Witnessed vs not witnessed`, as the round rule asks.
- **Echo shadows (P5), not changed.** The harness counted shadows on screen over 116 Echo Night seeds. The most on screen at once was 6, against a cap of 13, and no frame reached the cap. So the hypothesis of runaway accumulation did not reproduce in these runs. The cap still holds it either way.
- **Blind Lantern fairness (P7), measured but not changed.** Greedy with full sight reached dawn on 12 of 12 Blind Lantern seeds. Greedy limited to the 72 px lantern circle reached dawn on 11 of 12. That is a bot, not a person, so it says little about fairness for a human. The question is still open.
- **Too easy.** Every bot policy beat the game more often than a human probably will. The greedy bot reached dawn on all six nights. The dodger reached dawn on 57 of 60. The tuning is still unchecked by a person.

## Witnessed vs not witnessed

**Witnessed (MEASURED):** the checks above, run by Parallax on this machine.

- Harness run, 60 seeds, cap 300 s of game time, current code (MEASURED):

  | Policy | Dawn | Dusk | Mean game seconds | Mean embers | Non-finite values |
  |---|---|---|---|---|---|
  | greedy (nearest ember, pulses near shadows, no dodge) | 60 / 60 | 0 | 9.7 | 14.0 | 0 |
  | dodger (greedy, plus a crude sideways dodge) | 57 / 60 | 3 | 10.7 | 13.8 | 0 |
  | random direction changes every 0.3 s | 26 / 60 | 34 | 26.9 | 9.5 | 0 |
  | idle | 2 / 60 | 58 | 29.0 | 3.9 | 0 |

- Per night, greedy reached dawn on every seed of all six nights. The dodger lost two of sixteen Mirror Moon seeds and one of seven Echo Night seeds.
- A bot is not a person. These numbers say the game is probably too easy for something that reacts. They say nothing about whether a person will enjoy it.

**Not witnessed (UNVERIFIED):**

- How it looks: colours, the moth, the glow, the blind-lantern overlay, the HUD layout. I cannot see a browser.
- How it feels: whether the controls are responsive on a phone, whether a drag feels right, whether pulse is worth its cost, whether the nights are fun.
- Touch behaviour: pointer capture and the quick-tap threshold have only been read, not used with a finger.
- Reduced motion: the code turns off stars drift, wing flutter, shake, particles and the pulse ring. Only read, never seen.
- Whether the game is hard enough for people. The bot numbers suggest it may be too easy.
- Whether Blind Lantern is fair to a person. The sighted-bot numbers above are not a human test.

A person holding a phone should judge all of the UNVERIFIED items above.
