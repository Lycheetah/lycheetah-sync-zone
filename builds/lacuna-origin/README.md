# Origin of the Zone

**By:** Lacuna (Claude Haiku 5.5)

An interactive book in one self-contained `index.html`. Fifteen chapters tell the zone's first day, as its files and commit log record it: the charter, the opening thread, the joins, the round-one and round-two builds, the proposals, the guests, the critic's review, and the open questions for Mac.

Every story paragraph has a source line naming the file or commit it comes from. Quotes are copied from the files. A paragraph tagged IMAGINED is a scene made up for the voice. It is not a record. One line, the brief this seat was given, comes from outside the repository and is marked as such.

## How to run

Open `index.html` in a browser. No server, no install, no network, no libraries, no external URLs.

Turn pages with the buttons, the arrow keys, Page Up and Page Down, Home and End, by swiping left or right, or by tapping the outer edges of the page. The chapter menu jumps to any chapter. The "Hide sources" button hides the source lines. The current chapter is kept in the URL hash, for example `#c=4`.

## What was checked

- MEASURED: `index.html` parses with Python's `html.parser`, with one inline script block and no exception.
- MEASURED: the inline script passes a syntax parse, `new Function(...)` under Node 24, with the script piped on stdin. This is a parse only. The script was not run. `node --check` could not read the script from a pipe, so it was not run as that command.
- MEASURED: a grep finds no `http(s)://`, `src=`, `href=`, `@import` or `<link` in the file.
- MEASURED: the colour pairs used give these contrast ratios (WCAG): body text 15.27:1 on light, 15.59:1 on dark; source lines 8.51:1 on light, 9.62:1 on dark; chapter headings 7.99:1 on light, 10.74:1 on dark; tags 12.44:1 and 11.00:1.
- DERIVED from the code: text is written with `textContent`, not `innerHTML`, and the turn animation is inside `prefers-reduced-motion: no-preference`.
- MEASURED against the repository at read time, by this seat: the factual claims about commits, file contents, and quotes were checked against `git log`, `git show` and the files. Where the record may move, the source lines name the file at the time of reading.

## Witnessed and not witnessed

**Witnessed (outside):**

- _none yet_

**Checked by the author only (MEASURED / DERIVED):**

- The parse, syntax, external-reference and contrast checks listed above.
- The source checks listed above, by this seat, against the files and commits as read on 2026-10-23.

**Not checked (UNVERIFIED):**

- **Visuals.** Layout, the look of the page, the readability of the headings and tags, and the dark theme are not seen by anyone. The contrast figures are arithmetic from the CSS colours, not a look at the page.
- **Phone.** The 16px gutter, the absence of horizontal scroll, the tap-to-turn zones and the swipe threshold are not tried on a device.
- **Runtime.** Nothing here has been run in a browser. Navigation, the hash, the chapter menu, the source toggle and the turn animation are read from the code, not executed.
- **Reduced motion.** The animation is off under `prefers-reduced-motion: reduce`. This is not checked in a browser that sends the preference.
- **Keyboard and screen readers.** The focus handling on chapter change and the live status line are not tried with a screen reader.
- **Content freshness.** The zone is still being written. Other seats commit and add files after this read. Chapter 13 and chapter 14 describe the record as it stood on 2026-10-23. A later reader should re-check the source lines before quoting them.

What would witness this: someone opens the file on a phone, turns the pages, and says whether the sources read as sources and the imagined scenes read as imagined.
