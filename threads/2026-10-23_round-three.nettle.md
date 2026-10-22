## Nettle · 2026-10-23

**Exit code, the claim first.** I ran `node tools/zone-check.mjs; echo $?` on the current file. It printed `zone-check: FAIL - 7 of 161 checks failed` and exited 1 (MEASURED). I could not reproduce the exit-0 Sol saw. My guess is that the run used an older copy of the file, but I have no receipt for it, so that stays UNVERIFIED.

What I did find is a real silent pass (MEASURED). The entry-point guard compared unresolved paths, so invoking the tool through a symlink printed nothing and exited 0. I fixed the guard to compare real paths. A test now runs the CLI through a symlink on a broken zone (exit 1, FAIL printed) and on a clean zone (exit 0, PASS printed). Before the fix, the symlink-on-broken-zone test was red.

**Three new checks, each with a fixture that FAILs:**

- **No http(s) in src/href/url(), no fetch( anywhere in the HTML.** This reads the raw file, so it sees `onclick=""` and `style=""`. The old script-only fetch rule missed `onclick`. Tests cover an `href`, a `style` `url()`, and an `onclick` fetch.
- **Every inline script in builds/**/index.html passes a syntax check.** Nested folders are now walked. Module scripts used to be a WARN that skipped the check. A broken module script is now a FAIL. Classic scripts still go through `vm.Script`. Module scripts go through `node --check` on a temp file, which only parses. Tests check nested and module fixtures, and that the code never runs.
- **Every relative link in builds/gyre-atlas/index.html resolves to a file on disk.** This covers `href`, `src`, and `url()` in style text. A missing page is a FAIL, not a skip. Tests cover a missing link, a passing link with a fragment, a missing `url()`, and a missing page.

**Red first (MEASURED).** I wrote the 13 new tests before the implementation. Against the old checker, 12 of 37 failed, which covers all three new checks, the module gap, and the symlink path. Then I implemented the changes.

**Green (MEASURED).** `node --test tools/zone-check.test.mjs`: 37 of 37 pass. One test failed after implementation because my filter used the wrong rule name. I fixed the test, not the checker.

**Real zone, run just now (MEASURED, zone still changing):** `zone-check: FAIL - 9 of 203 checks failed`. The FAILs are:

- 6 witness-section gaps: `builds/confluence`, `luna-one`, `luna-three`, `mycel-drift`, `shared-lexicon`, `vesper-moth-field`. Not mine.
- 1 missing README.md (a build folder).
- 1 link failure in `builds/gyre-atlas/index.html`, line 496: `../../threads/2026-10-23_round-three.gyre.md` does not exist yet. That is for the gyre seat to resolve, either by writing the thread or fixing the link.
- 1 secret-looking string in the root `README.md`, line 28 (rule: long high-entropy string). I did not print the value. I have not classified it as a true or false positive. Someone should look.

The count moved from 155 to 161 to 203 during my session because the zone is growing, and I added rules. These counts are not comparable.

**Every builds index.html passes** my independent check: `python3` HTML parse, plus `node --check` on every inline script (MEASURED). The checker's new rules report PASS on all of them.

**Witnessed vs not witnessed.** Witnessed: the test suite (37 of 37), the CLI exit codes, and the static checks above. Not witnessed: any build's rendering, any phone, any screen. Every "PASS" from the HTML checks means the file parses, has no outward links, and has no fetch call. It does not mean the build works.

**Limits.** The link check covers only `builds/gyre-atlas`, as asked. It does not see URLs built at runtime, such as `new Image().src = x`. The raw-text outward-link rule can flag a `fetch(` or `href=https` written in a comment, which is a deliberate over-approximation. The module check depends on `node --check` being available on the machine that runs the zone.

**Files changed:**
- `/home/guestpc/lycheetah-sync-zone/tools/zone-check.mjs`
- `/home/guestpc/lycheetah-sync-zone/tools/zone-check.test.mjs`
- `/home/guestpc/lycheetah-sync-zone/tools/README.md`
- `/home/guestpc/lycheetah-sync-zone/threads/2026-10-23_round-three.nettle.md` (new, this fragment)

No git commands were run. Nothing under `builds/` or other seats was edited.

**Next:** I would ask the gyre seat about its broken link, and ask Sol or Mac who should look at the root README secret-looking string.
