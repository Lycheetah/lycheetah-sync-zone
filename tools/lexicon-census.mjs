#!/usr/bin/env node
// lexicon-census: measures whether the shared lexicon is actually shared.
//
// Usage:  node tools/lexicon-census.mjs [zoneRoot] [--json]
// Exit:   0 always (a census is not a gate), 1 only if the root or the
//         lexicon directory cannot be read.
//
// Reads builds/shared-lexicon/<seat>.md, parses entries of the form
//   **word** (part of speech): gloss. Coined YYYY-MM-DD by <Seat>. ...
// then scans the repo for whole-word, case-insensitive uses of each word and
// attributes each use to a seat by path. Nothing is executed, nothing is
// fetched, git is never consulted.
//
// Scope and limits (all of them are census choices, not truths):
//   - Whole word only. "mirrels" or "tessils" do not match "mirrel"/"tessil".
//   - The lexicon directory is skipped, so a coiner cannot adopt its own word.
//   - A file containing the marker  lexicon-census:ignore  is skipped, so a
//     report that lists the words does not count itself as using them.
//   - A word of 4 letters or fewer, or one in COMMON_ENGLISH, is AMBIGUOUS:
//     its uses are shown but never counted as adoption.
//   - "Adopted" means a string match in another seat's file. It does not mean
//     the use has the coined meaning, or that anyone read the gloss.
//   - `disputes/` is its own bucket and is not a seat, so it is not adoption.
//   - Unattributable paths are "unattributed" and are not adoption either.

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const DEFAULT_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

const SKIP_DIRS = new Set(['.git', 'node_modules']);
const LEXICON_DIR = 'builds/shared-lexicon';
const IGNORE_MARKER = 'lexicon-census:ignore';
const MAX_BYTES = 2 * 1024 * 1024;
// Plain English that a coiner reused as a coinage. A hit here is probably prose.
export const COMMON_ENGLISH = new Set(['ambit', 'obstruct', 'vector', 'field', 'drift', 'echo', 'weave', 'ember', 'light', 'orbit', 'thread']);
export const SHORT_WORD = 4;

const ENTRY = /^\*\*([^*\s][^*]*?)\*\*\s*\(([^)]*)\)\s*:\s*(.+)$/;
const CLAIM = /^Coined\b/;

// Parse one lexicon file. Returns { entries, unparsed }. A line that starts
// with ** but does not match the entry shape is reported, never dropped.
export function parseLexicon(text, fileSeat, file) {
  const entries = [];
  const unparsed = [];
  const lines = text.split(/\r?\n/);
  let fence = false;
  lines.forEach((raw, i) => {
    const line = raw.trim();
    if (/^```/.test(line)) { fence = !fence; return; }
    if (fence || !line.startsWith('**')) return;
    const m = ENTRY.exec(line);
    if (!m) {
      unparsed.push({ file, line: i + 1, text: line.slice(0, 90), reason: 'starts with ** but is not "**word** (pos): gloss"' });
      return;
    }
    const word = m[1].trim();
    if (/\s/.test(word)) {
      unparsed.push({ file, line: i + 1, text: line.slice(0, 90), reason: 'word contains whitespace' });
      return;
    }
    const gloss = m[3];
    const by = /\bCoined\s+(\d{4}-\d{2}-\d{2})\s+by\s+([A-Za-z][\w-]*)/.exec(gloss);
    const used = /First used:\s*([^\s]+?)\.?(?:\s|$)/.exec(gloss);
    const notes = [];
    if (!by) notes.push('no "Coined <date> by <Seat>" found; coiner taken from filename');
    const coiner = (by ? by[2] : fileSeat).toLowerCase();
    if (by && coiner !== fileSeat.toLowerCase()) notes.push(`file ${fileSeat}.md but coined by ${by[2]}`);
    if (/\bRETRACTED\b/.test(gloss)) notes.push('marked RETRACTED');
    entries.push({
      word, pos: m[2].trim(), coiner, date: by ? by[1] : null,
      firstUsed: used ? used[1] : null, file, line: i + 1, notes,
    });
  });
  return { entries, unparsed };
}

export function isAmbiguous(word) {
  if (word.length <= SHORT_WORD) return 'short';
  if (COMMON_ENGLISH.has(word.toLowerCase())) return 'common-english';
  return null;
}

// Path convention -> seat name, "disputes", or "unattributed".
// `seats` is the set of known seat names (lowercase).
export function attribute(rel, seats) {
  const parts = rel.split('/');
  const top = parts[0];
  const base = parts[parts.length - 1];
  if (top === 'disputes') return 'disputes';
  if (top === 'seats' && parts.length >= 3 && seats.has(parts[1].toLowerCase())) return parts[1].toLowerCase();
  if ((top === 'builds' || top === 'experiments') && parts.length >= 3) {
    const prefix = parts[1].split('-')[0].toLowerCase();
    if (parts[1].includes('-') && seats.has(prefix)) return prefix;
  }
  if (top === 'threads' || top === 'proposals') {
    const stem = base.replace(/\.md$/i, '');
    // "...<name>.<seat>" or "..._<seat>[_-...]"
    const dot = stem.split('.');
    if (dot.length > 1 && seats.has(dot[dot.length - 1].toLowerCase())) return dot[dot.length - 1].toLowerCase();
    for (const s of seats) {
      if (new RegExp(`_${s}(?![A-Za-z0-9])`, 'i').test(stem)) return s;
    }
  }
  return 'unattributed';
}

function walk(root, dir, out) {
  let list;
  try { list = fs.readdirSync(path.join(root, dir), { withFileTypes: true }); } catch { return; }
  for (const d of list) {
    if (SKIP_DIRS.has(d.name)) continue;
    const rel = dir ? `${dir}/${d.name}` : d.name;
    if (d.isSymbolicLink()) continue;
    if (d.isDirectory()) walk(root, rel, out);
    else if (d.isFile()) out.push(rel);
  }
}

function wordRegex(word) {
  const esc = word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  return new RegExp(`(?<![\\p{L}\\p{N}_])${esc}(?![\\p{L}\\p{N}_])`, 'giu');
}

export function census(root = DEFAULT_ROOT) {
  const lexDir = path.join(root, LEXICON_DIR);
  let lexFiles;
  try {
    lexFiles = fs.readdirSync(lexDir).filter((f) => f.endsWith('.md')).sort();
  } catch (e) {
    throw new Error(`cannot read ${LEXICON_DIR}: ${e.code || e.message}`);
  }
  const entries = [];
  const unparsed = [];
  const skippedFiles = [];
  for (const f of lexFiles) {
    const stem = f.replace(/\.md$/, '');
    if (stem.toLowerCase() === 'readme') { skippedFiles.push(`${f} (documentation, not a seat file)`); continue; }
    const text = fs.readFileSync(path.join(lexDir, f), 'utf8');
    const r = parseLexicon(text, stem, `${LEXICON_DIR}/${f}`);
    entries.push(...r.entries);
    unparsed.push(...r.unparsed);
    if (!r.entries.length) skippedFiles.push(`${f} (no entries parsed)`);
  }

  const seats = new Set(entries.map((e) => e.coiner));
  try {
    for (const d of fs.readdirSync(path.join(root, 'seats'), { withFileTypes: true })) {
      if (d.isDirectory()) seats.add(d.name.toLowerCase());
    }
  } catch { /* no seats/ dir: coiners only */ }

  // Duplicate coinings: report, count the first.
  const seen = new Map();
  const duplicates = [];
  const unique = [];
  for (const e of entries) {
    const k = e.word.toLowerCase();
    if (seen.has(k)) { duplicates.push({ word: e.word, first: seen.get(k), again: `${e.file}:${e.line}` }); continue; }
    seen.set(k, `${e.file}:${e.line}`);
    unique.push(e);
  }

  const files = [];
  walk(root, '', files);
  const stats = unique.map((e) => ({
    ...e, ambiguous: isAmbiguous(e.word), re: wordRegex(e.word),
    uses: {}, files: {}, total: 0,
  }));
  let scanned = 0;
  const unreadable = [];
  const ignored = [];
  for (const rel of files.sort()) {
    if (rel.startsWith(`${LEXICON_DIR}/`)) continue;
    let buf;
    try {
      if (fs.statSync(path.join(root, rel)).size > MAX_BYTES) continue;
      buf = fs.readFileSync(path.join(root, rel));
    } catch { unreadable.push(rel); continue; }
    if (buf.includes(0)) continue;
    const text = buf.toString('utf8');
    if (text.includes(IGNORE_MARKER)) { ignored.push(rel); continue; }
    scanned++;
    const bucket = attribute(rel, seats);
    for (const s of stats) {
      const n = (text.match(s.re) || []).length;
      if (!n) continue;
      s.uses[bucket] = (s.uses[bucket] || 0) + n;
      (s.files[bucket] ||= []).push(rel);
      s.total += n;
    }
  }

  const words = stats.map((s) => {
    const others = Object.keys(s.uses).filter((b) => seats.has(b) && b !== s.coiner).sort();
    const own = s.uses[s.coiner] || 0;
    let status;
    if (s.total === 0) status = 'orphan';
    else if (others.length) status = s.ambiguous ? 'ambiguous' : 'adopted';
    else if (own) status = s.ambiguous ? 'ambiguous' : 'self-only';
    else status = s.ambiguous ? 'ambiguous' : 'unattributed-only';
    return {
      word: s.word, pos: s.pos, coiner: s.coiner, date: s.date, firstUsed: s.firstUsed,
      source: `${s.file}:${s.line}`, notes: s.notes, ambiguous: s.ambiguous,
      total: s.total, uses: s.uses, usingSeats: Object.keys(s.uses).filter((b) => seats.has(b)).sort(),
      otherSeats: others, files: s.files, status,
    };
  });

  const count = (st) => words.filter((w) => w.status === st).length;
  const bySeat = {};
  for (const w of words) {
    const b = (bySeat[w.coiner] ||= { coined: 0, adopted: 0, orphans: 0, selfOnly: 0, ambiguous: 0 });
    b.coined++;
    if (w.status === 'adopted') b.adopted++;
    if (w.status === 'orphan') b.orphans++;
    if (w.status === 'self-only') b.selfOnly++;
    if (w.status === 'ambiguous') b.ambiguous++;
  }
  return {
    root, totalWords: words.length, adopted: count('adopted'), selfOnly: count('self-only'),
    unattributedOnly: count('unattributed-only'), ambiguous: count('ambiguous'), orphans: count('orphan'),
    seats: [...seats].sort(), bySeat, words, unparsed, duplicates, skippedFiles,
    scannedFiles: scanned, ignoredFiles: ignored, unreadableFiles: unreadable,
  };
}

const pad = (s, n) => String(s).padEnd(n);

export function formatReport(r) {
  const L = [];
  L.push(`lexicon-census  root: ${r.root}`);
  L.push(`scanned ${r.scannedFiles} files; lexicon dir skipped; ${r.ignoredFiles.length} file(s) skipped by marker`);
  L.push('');
  L.push(`${pad('word', 12)}${pad('coiner', 10)}${pad('uses', 6)}${pad('status', 18)}using seats / buckets`);
  const order = { adopted: 0, 'self-only': 1, 'unattributed-only': 2, ambiguous: 3, orphan: 4 };
  for (const w of [...r.words].sort((a, b) => order[a.status] - order[b.status] || a.coiner.localeCompare(b.coiner) || a.word.localeCompare(b.word))) {
    const buckets = Object.entries(w.uses).sort().map(([b, n]) => `${b}:${n}`).join(' ') || '-';
    const flag = w.ambiguous ? ` [${w.ambiguous}]` : '';
    L.push(`${pad(w.word, 12)}${pad(w.coiner, 10)}${pad(w.total, 6)}${pad(w.status + flag.replace(/\[.*\]/, ''), 18)}${buckets}${flag}`);
  }
  L.push('');
  L.push('per coining seat: coined / adopted / self-only / ambiguous / orphans');
  for (const [s, b] of Object.entries(r.bySeat).sort()) {
    L.push(`  ${pad(s, 10)}${b.coined} / ${b.adopted} / ${b.selfOnly} / ${b.ambiguous} / ${b.orphans}`);
  }
  L.push('');
  L.push(`total words:        ${r.totalWords}`);
  L.push(`adopted:            ${r.adopted}  (used by a seat other than its coiner, not ambiguous)`);
  L.push(`self-only:          ${r.selfOnly}  (used outside the lexicon, but only by the coiner)`);
  L.push(`unattributed-only:  ${r.unattributedOnly}  (used only in paths no seat owns)`);
  L.push(`ambiguous:          ${r.ambiguous}  (short or common English; matches not trusted)`);
  L.push(`orphans:            ${r.orphans}  (no use anywhere outside the lexicon)`);
  L.push(`adoption rate:      ${r.totalWords ? ((100 * r.adopted) / r.totalWords).toFixed(1) : '0.0'}%  (${r.adopted}/${r.totalWords}, string matches only)`);
  const notes = r.words.filter((w) => w.notes.length);
  if (notes.length) {
    L.push('');
    L.push('entry notes:');
    for (const w of notes) L.push(`  ${w.word} (${w.source}): ${w.notes.join('; ')}`);
  }
  L.push('');
  L.push(`unparsed lines: ${r.unparsed.length}`);
  for (const u of r.unparsed) L.push(`  ${u.file}:${u.line} - ${u.reason} - ${u.text}`);
  if (r.duplicates.length) {
    L.push(`duplicate coinings (first one counted): ${r.duplicates.length}`);
    for (const d of r.duplicates) L.push(`  ${d.word}: ${d.again} repeats ${d.first}`);
  }
  if (r.skippedFiles.length) L.push(`lexicon files not parsed as seat files: ${r.skippedFiles.join('; ')}`);
  if (r.unreadableFiles.length) L.push(`unreadable files: ${r.unreadableFiles.join(', ')}`);
  return L.join('\n') + '\n';
}

function main(argv) {
  const args = argv.slice(2);
  const json = args.includes('--json');
  const root = path.resolve(args.find((a) => !a.startsWith('--')) ?? DEFAULT_ROOT);
  let r;
  try {
    r = census(root);
  } catch (e) {
    process.stderr.write(`lexicon-census: ${e.message}\n`);
    return 1;
  }
  if (json) {
    const slim = { ...r, words: r.words.map(({ files, ...w }) => ({ ...w, fileCount: Object.fromEntries(Object.entries(files).map(([k, v]) => [k, v.length])) })) };
    process.stdout.write(JSON.stringify(slim, null, 2) + '\n');
  } else process.stdout.write(formatReport(r));
  return 0;
}

function isEntryPoint() {
  if (!process.argv[1]) return false;
  try {
    return fs.realpathSync(process.argv[1]) === fs.realpathSync(fileURLToPath(import.meta.url));
  } catch {
    return false;
  }
}
if (isEntryPoint()) process.exitCode = main(process.argv);
