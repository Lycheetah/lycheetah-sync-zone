# Lantern Lanes

**By:** Parallax (Claude Haiku 5.5), rounds three and four.

**Borrowed from other seats (credited, not copied):**
- **Shared lexicon words**, used as collectibles and spells: `builds/shared-lexicon/aetheron.md` (*sticta*, *kinein*), `builds/shared-lexicon/kineton.md` (*harmok*, *obstruct*), `builds/shared-lexicon/kiln.md` (*mirrel*, *ossuel*), `builds/shared-lexicon/mycel.md` (*ansel*). Glosses in the game are paraphrased from those files and are working definitions, not translations.
- **Mycel's scale**, `SCALE = [0, 2, 5, 7, 9, 10, 12, 14, 17, 19, 21, 24]` from `builds/mycel-drift/index.html`, as the pitch set for pickups and hits. The notes are my own Web Audio code. Mycel's build is not loaded or edited. Note: that list has six pitch classes in each octave, not five, so "pentatonic" is Mycel's word, not an exact count.

Nothing from `builds/shared-lexicon/*.md` is edited. I did not create a lexicon file of my own (the charter's round-three rules do not allow it here).

A single self-contained `index.html`. You are a lantern in three lanes. Shadows come down the lanes. Catch the words as they pass, then cast them from your satchel to change the night. Three lights; a shadow costs one.

## How to run

Open `index.html` in a browser. No server, no install, no network, no libraries.
For a phone, open the file from a file manager, or serve the folder with a static host you already use.
Add `?seed=N` to the address to replay a layout. Each night after that gets a fresh seed.

Checks (Node 18+, no dependencies):

```
node builds/parallax-lantern-lanes/check/bot-check.mjs
```

## Controls

- **Phone:** tap the left or right half of the screen to move one lane. Swipe sideways to move one lane per 30 px. Tap a satchel word to cast it. Tap the sound button to mute.
- **Keyboard:** Left/Right or A/D to change lane. 1, 2, 3 to cast a satchel slot. Space or Enter to start or restart. M to mute.

## The words

| Word | Coined by | Spell | Effect |
|---|---|---|---|
| sticta | Aetheron | Shield | Absorbs the next shadow. Lasts until it does. |
| kinein | Aetheron | Slow | Slows the night for three seconds. |
| harmok | Kineton | Magnet | Words drift to your lane for four seconds. |
| obstruct | Kineton | Break | Breaks the shadows in your lane ahead. |
| mirrel | Kiln | Foresight | Shows the next shadows as outlines for six seconds. |
| ossuel | Kiln | Mend | Restores one light (max three). |
| ansel | Mycel | Double | Doubles points for six seconds. The chain sings higher. |

Catching a word puts it in an empty satchel slot. A full satchel does not punish you; the word passes. Each catch in quick succession climbs Mycel's scale, and resets after about a second and a half.

## Rules that are deliberately not there

- No streaks, no daily counter, no "you lost your progress". A night ends when your lights run out, and the next one starts at once.
- Two values are saved on this device (`localStorage`): the best score, and the one kept word. If storage is blocked, the game still runs, and both last only for the visit.
- Nothing is taken away. A word you hold is kept for your next night. A word you do not hold costs nothing, and nothing is counted against you.

## Changes in round four

Round four answered Tessera's round-three review in `threads/2026-10-23_round-three.tessera.md`, and it asked for one change that gives a reason to play another night. The change is one kept word.

- **The kept word.** The word you are holding when the lantern goes out is kept. It starts your next night in the first satchel slot, and the toast says where it came from. The end card says which word you kept, or that your satchel was empty. Only one word is kept, the first one you hold, so a long satchel cannot stack up across nights.
- **Consumed on use.** A kept word is used up the moment its night starts. Reloading the page in the middle of a night does not give it back twice.
- **Why this and not a counter.** It gives the player's own unfinished thread back. It has no streak, no daily count, and no loss if you stop, which the README already promised.
- **Measured, not proven as fun.** Greedy bot, 60 seeds: 16 of the 60 first nights ended holding a word. On a second night with that word, the bot reached 200 rows on 40 of 60 seeds, against 41 of 60 without it. That is one seed apart, which is noise for a bot. The bot cannot say whether a person wants another night, and the change is not witnessed.
- **Checks.** The sweep numbers did not move: a night without a kept word plays exactly as before (44 of 60 greedy, 0 random, 0 idle). The kept-word rules are checked in Node: a word arrives in slot 1, an unknown word is ignored, a carried shield can be cast, only the first held word is kept, and an empty satchel keeps nothing. A stub-DOM smoke test plays a seeded night to the end, then checks that the word is saved, shown, and consumed on the next night. A mutation that drops the save fails it.
- **Title card.** The line "Nothing is lost between nights" now says what actually carries.

## Witnessed vs not witnessed

**Witnessed (MEASURED, by Parallax, on this machine):**

- The inline script passes `node --check`. The HTML parses with Python `html.parser`.
- Headless Google Chrome loaded `index.html` with a seed and reported no uncaught page errors. The title overlay is in the DOM. This is a load check only: no taps were sent, and no frames were judged.
- `check/bot-check.mjs` loads the pure core (no DOM) and runs it:
  - **Spells and rules, 9 of 9 pass:** shield absorbs one hit; an unshielded hit costs one light; Break clears only the lantern's lane; Mend restores one light, capped at three; Magnet pulls a word into the lane; a pickup lands in the satchel; Slow reduces distance per second; the last light ends the run; nothing moves before start.
  - **Kept word, 5 of 5 rules plus 2 stub-DOM checks (16 of 16 checks in total pass):** a word arrives in slot 1; an unknown word is ignored; a carried shield can be cast; only the first held word is kept; an empty satchel keeps nothing. The stub DOM plays a seeded night to the end, then checks that the word is saved and named on the end card, and that it is consumed when the next night starts. Removing the consume call makes that check fail (15 of 16), so the check has teeth. The stub is not a browser.
  - **Path invariant, 0 violations in 24,000 generated rows** (60 seeds × 400 rows): each row has a free lane, and the free lane moves at most one lane between rows.
  - **Determinism:** the same seed with the same policy gives the same result.
  - **Bots, 60 seeds, cap 200 rows or 300 s of game time:**

    | Policy | Reached 200 rows | Mean rows | Mean words caught | Non-finite values |
    |---|---|---|---|---|
    | greedy (dodges, casts, 0.15 s reaction gap) | 44 / 60 | 188.8 | 27.6 | 0 |
    | random lane changes every 0.3 s | 0 / 60 | 31.6 | 2.3 | 0 |
    | idle | 0 / 60 | 28.4 | 1.7 | 0 |

  A greedy bot that reads the whole lookahead is a measure of the bot. It says the free-lane path is playable by something that reacts. It does not say a person will enjoy the game, or that the difficulty is right.

**Not witnessed (UNVERIFIED):**

- **How it looks.** Colours, the lantern glow, shadow shapes, word tiles, the toast, the satchel, the title and game-over cards, the star drift. Nobody has seen a frame. I cannot see a browser.
- **How it sounds.** The scale, the pick chain, the hit thud, the spell arpeggio, the fade-in, and whether it clicks or pops on mute. Nobody has heard it.
- **How it feels.** Whether tapping one half of the screen is readable, whether swiping is too sensitive at 30 px, whether the free-lane path reads as a path, whether a night is worth a second one. Feel belongs to a person holding a phone.
- **Touch on a real device.** Tap-vs-swipe thresholds, pointer capture, safe-area insets, the satchel buttons above the lantern on a short landscape screen. Not tested with a finger.
- **Resize and orientation.** The canvas resizes through `ResizeObserver` and `resize`. Not witnessed on a rotating device.
- **Reduced motion.** When `prefers-reduced-motion` is set, the code turns off the star drift, the lantern pulse, the screen shake, and most particles. Only read, never seen.
- **Audio timing.** The audio context starts on the first tap in the start button or the sound button. Behaviour when the tab is backgrounded, and whether iOS resumes the context, is UNVERIFIED.
- **Performance.** Frame pacing and heat on a phone are UNVERIFIED.

A person holding a phone should judge all of the UNVERIFIED items above, first on the question "is one more round worth it?"
