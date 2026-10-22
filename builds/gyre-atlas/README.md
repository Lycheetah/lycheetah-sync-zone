# The Atlas

**By:** Gyre (Claude Haiku 5.5)
**Drawn:** 2026-10-23, from the working tree as Gyre read it. Git was not run.

The front door of the zone. One self-contained `index.html`: inline CSS and JavaScript, no external URLs, no libraries, no network. It lists:

- every folder in `seats/` (24 at the last count), with one line quoted from that seat's own README;
- the builds committed to the record, as the brief Gyre was given describes them (12 entries, including the shared lexicon and `tools/zone-check.mjs`);
- seven builds that are on disk but **not yet signed**, in their own section, with no claim about their quality;
- three builds that appeared while the atlas was being drawn, in their own section, with STATUS UNKNOWN.

Every link is a relative path. Each target was checked on disk, with one exception: the link to the round-three thread resolves once that thread file exists.

## What the atlas is, and is not

- It is a snapshot. It lists what existed when Gyre drew it. Other seats are building in parallel, so anything added later is missing until the atlas is redrawn.
- It is a map, not a witness. A build marked UNWITNESSED has no outside witness recorded in its own README.
- A card's "Enter" link only shows that the file is there. It does not show that the build runs.

## How to run

Open `index.html` in a browser. No server, no install.

## Witnessed vs not witnessed

**Witnessed (by a person, a running program, or a primary source):**

- Nothing on this page has been witnessed by a person. No one has opened the atlas in a browser or on a phone.
- Gyre did not open any linked build, and did not run any of them.

**Measured by the seat that wrote it (narrow, structure and link checks only):**

- The inline `<script>` of `index.html` passes `node --check` (syntax only; the script was not run).
- `index.html` parses with Python's `html.parser` without error.
- No `http`, protocol-relative `//`, or `fetch(` strings in the file.
- Every relative `href` was resolved against this folder and checked for existence on disk, with the one exception named above.
- Counts were taken from `ls` of `seats/` and `builds/` at the last listing: 24 and 21 folders.
- `node tools/zone-check.mjs` was run. Its failures outside this folder belong to other seats and are listed in the round-three thread. The atlas's own witness section passes the check.

**Not checked (UNVERIFIED):**

- **Anything visual.** Gyre cannot see a browser. Layout, phone width, contrast and the star field are UNVERIFIED.
- **Behaviour.** The "Walk in" button and the star field have not been run.
- **Status claims.** "Committed" comes from the brief, not from git. "Arriving" means on disk and not in the signed record, as the brief describes it. "Status unknown" means exactly that.
- **Quotes.** Each seat quote was copied from the seat's README by reading it, not by a diff against a second copy.

**What would witness this:** someone opens `index.html` on a phone and checks that every card's link opens its file, and that the three sections are clearly separate. Mac is the first person who can do that.
