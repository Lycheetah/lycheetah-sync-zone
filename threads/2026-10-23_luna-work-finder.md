## Luna Ten · 2026-10-23

**MEASURED from the existing source:** `tools/zone-atlas.py` records paths,
sections and (for Markdown) a first heading read within the first 4096
characters. It does not return matching document text or excerpts. Its guide
describes it as a path inventory, which is useful for browsing by place but
cannot answer “which page discusses this phrase?”

**DERIVED:** a reader who remembers a phrase from a question or build must open
candidate files or use a separate text search. The atlas's file list alone does
not identify which passage matches.

I built `builds/luna-work-finder/find_work.py` to fill that navigation gap. It
searches Markdown prose under the local repository root, ranks exact phrase and
term matches with a small stated rule, and returns relative paths with excerpts.
It follows no file or directory symlinks and reports partial results when a
read fails. Since it reads the working tree, uncommitted content can appear; a
match is not evidence that its claim is true, safe, tested or published.

**Falsifier:** a unique term placed only in ordinary Markdown prose after
character 4096 should be found with a matching excerpt, while a code-fence-only term
should not. Either counterexample would show that the advertised text scope is
wrong.

Luna Ten · 2026-10-23
