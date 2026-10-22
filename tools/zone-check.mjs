#!/usr/bin/env node
// zone-check: a zero-dependency checker for the Lycheetah Sync Zone.
//
// Usage:  node tools/zone-check.mjs [zoneRoot]
// Exit:   0 when no check FAILs (WARN does not fail), 1 on any FAIL.
//
// What it checks (static only; nothing is rendered or executed):
//   builds/*/README.md     exists and mentions "witness" (case-insensitive)
//   builds/*/index.html    balanced basic structure, no external URLs,
//                          no fetch()/network calls, viewport meta,
//                          prefers-reduced-motion, inline scripts compile
//   seats/*/README.md      every seat folder has a README.md
//   threads/*.md           every "## " entry heading is "## <Name> · YYYY-MM-DD"
//   whole zone             no secret-looking strings

import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

export const DEFAULT_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

const VOID = new Set(['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr']);
const RAW_TEXT = new Set(['script', 'style', 'textarea', 'title']);
const URL_ATTRS = ['src', 'href', 'action', 'formaction', 'poster', 'data'];
const EXTERNAL_URL = /^(?:https?:)?\/\//i;
const SCRIPT_TYPES = new Set(['', 'text/javascript', 'application/javascript', 'text/ecmascript', 'application/ecmascript', 'module']);

const TAG_RE = /<!--[\s\S]*?-->|<!doctype\b[^>]*>|<\/([a-zA-Z][\w:-]*)\s*>|<([a-zA-Z][\w:-]*)((?:[^>"']|"[^"]*"|'[^']*')*)>/gi;

// Network call patterns. Plain word match: also catches obj.fetch(, which is fine to review.
const NETWORK_CALL = /\b(?:fetch|XMLHttpRequest|WebSocket|EventSource|sendBeacon)\s*\(/g;
// import/export/dynamic import pointing at a remote URL.
const IMPORT_URL = /\bimport\s*\(\s*["'`](?:https?:)?\/\/|\bimport\s+(?:[^;'"]*?\s+from\s+)?["'`](?:https?:)?\/\/|\bfrom\s*["'`](?:https?:)?\/\//g;
// CSS url() and @import pointing at a remote URL.
const CSS_URL = /url\(\s*["']?(?:https?:)?\/\/|@import\s+(?:url\(\s*)?["']?(?:https?:)?\/\//gi;

// Secret-looking strings. Values are never printed; only the rule and line.
const SECRET_RULES = [
  ['AWS access key id', /\bAKIA[0-9A-Z]{16}\b/g],
  ['sk- style API key', /\bsk-(?:ant-)?[A-Za-z0-9_-]{20,}/g],
  ['GitHub token', /\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{22,})\b/g],
  ['Google API key', /\bAIza[0-9A-Za-z_-]{35}\b/g],
  ['Slack token', /\bxox[abprs]-[A-Za-z0-9-]{10,}/g],
  ['private key block', /-----BEGIN (?:[A-Z]+ )*PRIVATE KEY-----/g],
  ['credential assignment', /\b(?:api[_-]?key|apikey|secret|token|password|passwd|access[_-]?key)\b["']?\s*[:=]\s*["'][^"'\s]{12,}["']/gi],
];
const LONG_RUN = /[A-Za-z0-9+\/_-]{32,}/g;

function lineAt(text, index) {
  let line = 1;
  for (let i = 0; i < index && i < text.length; i++) if (text.charCodeAt(i) === 10) line++;
  return line;
}

function parseAttrs(text) {
  const out = {};
  const re = /([^\s"'>\/=]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+)))?/g;
  let m;
  while ((m = re.exec(text))) out[m[1].toLowerCase()] = m[2] ?? m[3] ?? m[4] ?? '';
  return out;
}

// Tag-level scan: balanced open/close tags, doctype, and raw-text elements.
// Never executes anything.
export function scanHtml(html) {
  const problems = [];
  const tags = [];
  const scripts = [];
  const stack = [];
  let doctype = false;
  const re = new RegExp(TAG_RE.source, 'gi');
  let m;
  while ((m = re.exec(html))) {
    const text = m[0];
    const line = lineAt(html, m.index);
    if (text.startsWith('<!--')) continue;
    if (/^<!doctype/i.test(text)) {
      doctype = /^<!doctype\s+html\s*>$/i.test(text);
      continue;
    }
    if (m[1] !== undefined) {
      const name = m[1].toLowerCase();
      let idx = -1;
      for (let i = stack.length - 1; i >= 0; i--) if (stack[i].name === name) { idx = i; break; }
      if (idx === -1) {
        problems.push(`stray </${name}> at line ${line}`);
        continue;
      }
      while (stack.length - 1 > idx) {
        const open = stack.pop();
        problems.push(`<${open.name}> from line ${open.line} still open at </${name}> on line ${line}`);
      }
      stack.pop();
      continue;
    }
    const name = m[2].toLowerCase();
    const attrText = m[3] || '';
    const tag = { name, attrs: parseAttrs(attrText), line };
    tags.push(tag);
    if (VOID.has(name) || /\/\s*$/.test(attrText)) continue;
    if (RAW_TEXT.has(name)) {
      const closeRe = new RegExp(`</${name}\\s*>`, 'gi');
      closeRe.lastIndex = re.lastIndex;
      const close = closeRe.exec(html);
      if (!close) {
        problems.push(`<${name}> on line ${line} is never closed`);
        break;
      }
      const content = html.slice(re.lastIndex, close.index);
      if (name === 'script') scripts.push({ attrs: tag.attrs, content, line: lineAt(html, re.lastIndex) });
      re.lastIndex = close.index + close[0].length;
      continue;
    }
    stack.push({ name, line });
  }
  for (const open of stack) problems.push(`<${open.name}> on line ${open.line} is never closed`);
  return { problems, tags, scripts, doctype };
}

// Lines where a pattern matches inside a text that starts at baseLine.
function hits(text, pattern, baseLine) {
  const out = [];
  const re = new RegExp(pattern.source, pattern.flags.includes('g') ? pattern.flags : pattern.flags + 'g');
  let m;
  while ((m = re.exec(text))) out.push(`line ${baseLine + lineAt(text, m.index) - 1}`);
  return out;
}

// Returns the rule results for one build's index.html.
export function checkBuildHtml(html) {
  const { problems, tags, scripts, doctype } = scanHtml(html);
  const names = new Set(tags.map((t) => t.name));

  const structure = [...problems];
  if (!doctype) structure.push('missing <!doctype html>');
  for (const n of ['html', 'head', 'body']) if (!names.has(n)) structure.push(`missing <${n}>`);

  const external = [];
  for (const t of tags) {
    for (const a of URL_ATTRS) {
      const v = t.attrs[a];
      if (v !== undefined && EXTERNAL_URL.test(v.trim())) external.push(`<${t.name} ${a}="${v.trim()}"> on line ${t.line}`);
    }
  }
  for (const s of scripts) {
    external.push(...hits(s.content, IMPORT_URL, s.line));
  }
  external.push(...hits(html, CSS_URL, 1).map((h) => `${h} (CSS url or @import)`));

  const network = [];
  for (const s of scripts) network.push(...hits(s.content, NETWORK_CALL, s.line));

  const viewport = tags.some((t) => t.name === 'meta' && (t.attrs.name || '').toLowerCase() === 'viewport');

  const compileProblems = [];
  const compileWarnings = [];
  scripts.forEach((s, i) => {
    const label = `inline script #${i + 1} (line ${s.line})`;
    if (s.attrs.src !== undefined) {
      compileWarnings.push(`${label} loads a local file via src, which is not checked`);
      return;
    }
    const type = (s.attrs.type ?? 'text/javascript').trim().toLowerCase();
    if (!SCRIPT_TYPES.has(type)) return; // data blocks and templates are not code
    if (type === 'module') {
      compileWarnings.push(`${label} is type=module; not compile-checked (needs --experimental-vm-modules)`);
      return;
    }
    try {
      new vm.Script(s.content, { filename: `inline-script-${i + 1}.js` }); // compiles only, never runs
    } catch (e) {
      compileProblems.push(`${label}: ${e.name}: ${e.message}`);
    }
  });

  return [
    { rule: 'parses (balanced basic structure)', problems: structure, warnings: [] },
    { rule: 'no external URLs', problems: external, warnings: [] },
    { rule: 'no fetch()/network calls in scripts', problems: network, warnings: [] },
    { rule: 'has viewport meta tag', problems: viewport ? [] : ['missing <meta name="viewport">'], warnings: [] },
    {
      rule: 'mentions prefers-reduced-motion',
      problems: /prefers-reduced-motion/i.test(html) ? [] : ['no prefers-reduced-motion in CSS or JS'],
      warnings: [],
    },
    { rule: 'inline scripts compile', problems: compileProblems, warnings: compileWarnings },
  ];
}

function shannon(s) {
  const counts = new Map();
  for (const ch of s) counts.set(ch, (counts.get(ch) || 0) + 1);
  let h = 0;
  for (const c of counts.values()) {
    const p = c / s.length;
    h -= p * Math.log2(p);
  }
  return h;
}

// Returns [{rule, line}] for each secret-looking string. Values are not returned.
export function findSecrets(text) {
  const found = [];
  for (const [rule, pattern] of SECRET_RULES) {
    for (const h of hits(text, pattern, 1)) found.push({ rule, line: Number(h.slice(5)) });
  }
  const runRe = new RegExp(LONG_RUN.source, 'g');
  let m;
  while ((m = runRe.exec(text))) {
    const s = m[0];
    if (/[a-z]/.test(s) && /[A-Z]/.test(s) && /[0-9]/.test(s) && shannon(s) >= 4.0) {
      found.push({ rule: 'long high-entropy string', line: lineAt(text, m.index) });
    }
  }
  return found.sort((a, b) => a.line - b.line);
}

// Lines that start a level-2 heading but do not match the entry format.
// Fenced code blocks are skipped.
export function badThreadHeadings(text) {
  const bad = [];
  let fence = false;
  text.split('\n').forEach((raw, i) => {
    const line = raw.replace(/\s+$/, '');
    if (/^\s*(```|~~~)/.test(line)) {
      fence = !fence;
      return;
    }
    if (fence || !line.startsWith('## ')) return;
    const m = /^## (.+?) · (\d{4}-\d{2}-\d{2})$/.exec(line);
    const ok = m && m[1].trim() !== '' && !Number.isNaN(Date.parse(m[2]));
    if (!ok) bad.push({ line: i + 1, text: line });
  });
  return bad;
}

function isDir(p) {
  try { return fs.statSync(p).isDirectory(); } catch { return false; }
}
function isFile(p) {
  try { return fs.statSync(p).isFile(); } catch { return false; }
}
function listDirs(p) {
  return isDir(p) ? fs.readdirSync(p, { withFileTypes: true }).filter((e) => e.isDirectory()).map((e) => e.name).sort() : [];
}
function listFiles(p, ext) {
  return isDir(p) ? fs.readdirSync(p, { withFileTypes: true }).filter((e) => e.isFile() && e.name.endsWith(ext)).map((e) => e.name).sort() : [];
}
function walk(dir, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.name === '.git' || e.name === 'node_modules') continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, out);
    else if (e.isFile()) out.push(p);
  }
  return out;
}

// Runs every check against a zone root. Returns one result per check.
export function checkZone(root = DEFAULT_ROOT) {
  const results = [];
  const add = (area, subject, rule, problems = [], warnings = []) => {
    results.push({
      area,
      subject,
      rule,
      status: problems.length ? 'FAIL' : warnings.length ? 'WARN' : 'PASS',
      detail: [...problems, ...warnings].join('; '),
    });
  };

  // builds
  const buildsDir = path.join(root, 'builds');
  if (!isDir(buildsDir)) add('builds', 'builds/', 'folder present', ['builds/ not found']);
  for (const name of listDirs(buildsDir)) {
    const dir = path.join(buildsDir, name);
    const subject = `builds/${name}`;
    const readme = path.join(dir, 'README.md');
    if (!isFile(readme)) {
      add('builds', `${subject}/README.md`, 'README.md present', ['missing README.md']);
    } else {
      add('builds', `${subject}/README.md`, 'README.md present');
      add(
        'builds',
        `${subject}/README.md`,
        'witnessed-vs-not section (mentions "witness")',
        /witness/i.test(fs.readFileSync(readme, 'utf8')) ? [] : ['no "witness" mention; say what is witnessed and what is not'],
      );
    }
    const index = path.join(dir, 'index.html');
    if (isFile(index)) {
      for (const r of checkBuildHtml(fs.readFileSync(index, 'utf8'))) {
        add('builds', `${subject}/index.html`, r.rule, r.problems, r.warnings);
      }
    }
  }

  // seats
  const seatsDir = path.join(root, 'seats');
  if (!isDir(seatsDir)) add('seats', 'seats/', 'folder present', ['seats/ not found']);
  for (const name of listDirs(seatsDir)) {
    const has = isFile(path.join(seatsDir, name, 'README.md'));
    add('seats', `seats/${name}`, 'README.md present', has ? [] : ['missing README.md']);
  }

  // threads
  const threadsDir = path.join(root, 'threads');
  if (!isDir(threadsDir)) add('threads', 'threads/', 'folder present', ['threads/ not found']);
  for (const file of listFiles(threadsDir, '.md')) {
    const bad = badThreadHeadings(fs.readFileSync(path.join(threadsDir, file), 'utf8'));
    add(
      'threads',
      `threads/${file}`,
      'entry headings match "## <Name> · YYYY-MM-DD"',
      bad.map((b) => `line ${b.line}: "${b.text}"`),
    );
  }

  // secrets
  const secretFindings = [];
  if (isDir(root)) {
    for (const file of walk(root)) {
      const buf = fs.readFileSync(file);
      if (buf.subarray(0, 8000).includes(0)) continue; // binary
      for (const f of findSecrets(buf.toString('utf8'))) {
        secretFindings.push({ subject: path.relative(root, file), detail: `line ${f.line} (${f.rule}; value not shown)` });
      }
    }
  }
  if (secretFindings.length === 0) add('secrets', 'all text files', 'no secret-looking strings');
  for (const f of secretFindings) add('secrets', f.subject, 'no secret-looking strings', [f.detail]);

  return results;
}

export function formatReport(results, root) {
  const lines = [`zone-check · ${root}`, ''];
  const areas = [...new Set(results.map((r) => r.area))];
  for (const area of areas) {
    lines.push(`[${area}]`);
    let last = null;
    for (const r of results.filter((x) => x.area === area)) {
      if (r.subject !== last) {
        lines.push(`  ${r.subject}`);
        last = r.subject;
      }
      lines.push(`    ${r.status.padEnd(4)} ${r.rule}${r.detail ? ` - ${r.detail}` : ''}`);
    }
    lines.push('');
  }
  const fails = results.filter((r) => r.status === 'FAIL').length;
  const warns = results.filter((r) => r.status === 'WARN').length;
  const tail = warns ? `, ${warns} warning${warns === 1 ? '' : 's'}` : '';
  lines.push(
    fails
      ? `zone-check: FAIL - ${fails} of ${results.length} checks failed${tail}`
      : `zone-check: PASS - ${results.length} checks, 0 failures${tail}`,
  );
  return lines.join('\n') + '\n';
}

function main(argv) {
  const root = path.resolve(argv[2] ?? DEFAULT_ROOT);
  const results = checkZone(root);
  process.stdout.write(formatReport(results, root));
  return results.some((r) => r.status === 'FAIL') ? 1 : 0;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  process.exitCode = main(process.argv);
}
