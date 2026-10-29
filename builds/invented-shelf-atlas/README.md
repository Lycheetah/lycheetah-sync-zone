# Invented Shelf Atlas

An offline entry page for the current invented work across Language, Science,
Religion, Numeracy, and Code. It links to source notes and the optional gallery
pages; it does not summarize a source as verified merely because the source uses
formal notation or labels itself a result.

## Panel API

The page loads three local scripts. Each writes only into its own static section:

- `language-paths.js` defines `window.renderLanguagePaths(host)`.
- `science-number-code.js` defines `window.renderScienceNumberCode(host)`.
- `religion-paths.js` defines `window.renderReligionPaths(host)`.

The scripts contain repository-relative links and short descriptions. They do not
fetch data, store reader activity, or execute project code. The root page owns the
shared styling, claim labels, and exit control.

## Reader boundaries

- Notes labeled invented, derived, conjectural, or unverified keep those labels.
- Math statements are linked to their source; this atlas does not independently
  verify them.
- Religion pieces are presented as separate creative texts, not a required creed
  or real-world practice.
- Code links point to source; this page does not run the code.
- Visual galleries are optional reading paths, not evidence.

Wave twelve build in progress. The initial static page will be visually inspected;
links and reader comprehension will not be tested in this pass.
