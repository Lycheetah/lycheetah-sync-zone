// Logic run of Glossolith's inline script against a stub DOM. No browser.
// Usage: node builds/kiln-glossolith/stub-check.mjs
// It proves logic only. It says nothing about layout, sound, touch or a screen reader.
import fs from 'node:fs';
import vm from 'node:vm';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const html = fs.readFileSync(path.join(here, 'index.html'), 'utf8');
const m = html.match(/<script>([\s\S]*?)<\/script>/);
if (!m) throw new Error('no inline script');
let code = m[1];

// Syntax: compile only, never run.
new vm.Script(code, { filename: 'glossolith-inline.js' });

// Expose internals to this harness only (not in the shipped file).
const hook = '  renderOut();\n  renderLexicon();\n})();';
if (!code.includes(hook)) throw new Error('hook anchor not found');
code = code.replace(hook, '  renderOut();\n  renderLexicon();\n  globalThis.__kiln = { tokens: function () { return tokens; }, lexicon: lexicon };\n})();');

// Seeded Math.random so drift is reproducible.
let seed = 12345;
Math.random = () => { seed = (seed * 1103515245 + 12345) & 0x7fffffff; return seed / 0x80000000; };

function makeEl(tag) {
  const el = {
    tagName: tag, children: [], attrs: {}, listeners: {}, style: {}, disabled: false, type: '',
    classList: { set: new Set(), add(c) { this.set.add(c); }, remove(c) { this.set.delete(c); } },
    _text: '',
    get textContent() { return this.children.length ? this.children.map(c => c.textContent).join('') : this._text; },
    set textContent(v) { this.children = []; this._text = String(v); },
    setAttribute(k, v) { this.attrs[k] = String(v); },
    getAttribute(k) { return k in this.attrs ? this.attrs[k] : null; },
    appendChild(c) { this._text = ''; this.children.push(c); return c; },
    addEventListener(t, f) { (this.listeners[t] ||= []).push(f); },
    querySelector(sel) {
      const mm = sel.match(/data-idx="(\d+)"/);
      const walk = (n) => { for (const c of (n.children || [])) { if (c.attrs && mm && c.attrs['data-idx'] === mm[1]) return c; const r = walk(c); if (r) return r; } return null; };
      return mm ? walk(this) : null;
    },
  };
  return el;
}

const ids = {};
for (const id of ['src', 'out', 'gloss', 'lex', 'drift', 'coin']) ids[id] = makeEl(id);
ids.src.value = '';
const docListeners = {};
const doc = {
  hidden: false,
  getElementById: (id) => ids[id] || (ids[id] = makeEl(id)),
  createElement: (t) => makeEl(t),
  createTextNode: (t) => ({ nodeType: 3, textContent: t }),
  addEventListener: (t, f) => { (docListeners[t] ||= []).push(f); },
};
const timeouts = new Map(); const intervals = new Map(); let nextId = 1;
const sandbox = {
  document: doc,
  window: { matchMedia: () => ({ matches: false }) },
  setTimeout: (fn, ms) => { const id = nextId++; timeouts.set(id, { fn, ms }); return id; },
  clearTimeout: (id) => timeouts.delete(id),
  setInterval: (fn, ms) => { const id = nextId++; intervals.set(id, { fn, ms }); return id; },
  clearInterval: (id) => intervals.delete(id),
  console, Math, Date, Map, Set, Array, Object, String, Number, JSON, Symbol, RegExp, Error,
};
vm.createContext(sandbox);
vm.runInContext(code, sandbox, { filename: 'glossolith-harness.js' });
const K = sandbox.__kiln;

let fails = 0;
function check(name, ok, detail = '') {
  console.log(`${ok ? 'PASS' : 'FAIL'} ${name}${detail ? ' :: ' + detail : ''}`);
  if (!ok) fails++;
}
const fire = (name, arg) => (docListeners[name] || []).forEach(f => f(arg));
const elFire = (el, name) => (el.listeners[name] || []).forEach(f => f({}));
const runPending = (ms) => { for (const [id, t] of [...timeouts]) if (t.ms === ms) { timeouts.delete(id); t.fn(); } };
const type = (text) => { ids.src.value = text; elFire(ids.src, 'input'); };

// K1: typing key by key must not write the lexicon.
const word = 'the river';
for (let i = 1; i <= word.length; i++) type(word.slice(0, i));
check('K1 keystrokes do not write the lexicon', K.lexicon.size === 0, `size=${K.lexicon.size}`);
runPending(1500);
// After the pause only closed words count. "the" is closed by the space; "river" is not.
const afterPause = [...K.lexicon.keys()];
check('K1 pause commits only closed words', afterPause.length === 1, `keys=${JSON.stringify(afterPause)}`);
const noFragments = afterPause.every(k => !['t', 'th', 'r', 'ri', 'riv'].includes(k.toLowerCase()));
check('K1 no half-typed fragments recorded', noFragments);
ids.src.value = 'the river';
elFire(ids.src, 'change');
check('K1 blur commits the last word', K.lexicon.size === 2, `size=${K.lexicon.size}`);
elFire(ids.src, 'change');
const counts1 = [...K.lexicon.values()].map(v => v.count);
check('K1 unchanged text is not counted twice', counts1.every(c => c === 1), `counts=${counts1}`);
check('K1 label says sentences, not keystrokes', !ids.lex.textContent.includes('x)') && !/heard \d+x/.test(ids.lex.textContent));

// K3: non-ASCII letters are transmuted, not passed through.
ids.src.value = 'café naïve';
elFire(ids.src, 'input');
const formsK3 = K.tokens().filter(t => !t.punct).map(t => t.form);
check('K3 accented words fully transmuted', formsK3.length === 2 && formsK3.every(f => /^[A-Za-z]+$/.test(f)), `forms=${JSON.stringify(formsK3)}`);

// K4: the output region is not a live region.
check('K4 #out has no aria-live', ids.out.getAttribute('aria-live') === null);

// K2 + K7: drift changes one vowel of one word; consonants (incl. "ly") never change.
const sample = 'salty holy lyric family silly lyre slyly ally only daily early the river hunger echo moth';
type(sample);
runPending(1500);
const snap = () => K.tokens().filter(t => !t.punct).map(t => t.parts.syl.map(s => s.c).join('|') + '#' + t.parts.coda);
const before = snap();
const formsBefore = K.tokens().filter(t => !t.punct).map(t => t.form);
const btnBefore = ids.out.children.filter(c => c.attrs && c.attrs['data-idx'] !== undefined);
elFire(ids.drift, 'click');
check('K5 drift starts', (ids.drift.getAttribute('aria-pressed') === 'true'));
let consonantBreaks = 0, multiChange = 0, ticks = 0;
const iv = [...intervals.values()][0];
for (let i = 0; i < 2000; i++) {
  const prev = K.tokens().filter(t => !t.punct).map(t => t.form);
  iv.fn(); ticks++;
  const now = K.tokens().filter(t => !t.punct).map(t => t.form);
  const changed = now.filter((f, j) => f !== prev[j]).length;
  if (changed > 1) multiChange++;
  if (JSON.stringify(snap()) !== JSON.stringify(before)) consonantBreaks++;
}
check('K2 consonants (incl. "ly") never changed over 2000 ticks', consonantBreaks === 0, `breaks=${consonantBreaks}`);
check('K2 at most one word changes per tick', multiChange === 0, `multi=${multiChange}`);
check('K2 drift does change forms', K.tokens().filter(t => !t.punct).map(t => t.form).join() !== formsBefore.join(), '');
const btnAfter = ids.out.children.filter(c => c.attrs && c.attrs['data-idx'] !== undefined);
check('K7 word elements are kept (focus survives drift)', btnAfter.length === btnBefore.length && btnAfter.every((b, i) => b === btnBefore[i]));

// K5: hidden tab stops ticking; visible resumes.
doc.hidden = true; fire('visibilitychange');
check('K5 hidden tab stops the drift timer', intervals.size === 0);
doc.hidden = false; fire('visibilitychange');
check('K5 visible tab resumes the drift timer', intervals.size === 1);
elFire(ids.drift, 'click');
check('K5 drift stops on request', intervals.size === 0 && ids.drift.getAttribute('aria-pressed') === 'false');

console.log(fails ? `RESULT: ${fails} FAIL` : 'RESULT: all logic checks pass (no browser, no screen, no sound)');
process.exit(fails ? 1 : 0);
