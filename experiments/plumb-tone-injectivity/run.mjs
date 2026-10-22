// Plumb, 2026-10-23. Port of Mycel's paramsOf (builds/mycel-lexical-tones/index.html).
// No network. Reads only local files.
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const ZONE = '/home/guestpc/lycheetah-sync-zone';
const CONS = ['k','t','r','s','l','m','n','v','th','z','ph','x','gh','sh','ly','d'];
const VOW = ['a','e','i','o','u','ae','ou','ia','y','eo'];
const CODA = ['','','','n','s','th','r','k'];
const SCALE = [0,2,5,7,9,10,12,14,17,19,21,24];
const BASE = 146.83;
const VOWEL_CUTOFF = { a:900,e:1400,i:2200,o:600,u:400,ae:1200,ou:500,ia:1800,y:2000,eo:800 };

function hash(s) {
  let x = 2166136261;
  for (let i = 0; i < s.length; i++) {
    x ^= s.charCodeAt(i);
    x = Math.imul(x, 16777619) >>> 0;
  }
  return x >>> 0;
}
function rng(seed) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6D2B79F5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
function pick(r, arr) { return arr[Math.floor(r() * arr.length) % arr.length]; }
function formOf(word) {
  const key = word.toLowerCase();
  const r = rng(hash(key));
  const n = Math.min(4, 1 + Math.floor(key.length / 3));
  let f = '';
  for (let i = 0; i < n; i++) f += pick(r, CONS) + pick(r, VOW);
  return f + pick(r, CODA);
}
function paramsOf(word) {
  const key = word.toLowerCase();
  const h = hash('tone:' + key);
  const form = formOf(word);
  const semi = SCALE[h % SCALE.length];
  const octave = (h >>> 8) % 2;
  const freq = BASE * Math.pow(2, (semi + 12 * octave) / 12);
  const vm = form.match(/(ae|ou|ia|eo|a|e|i|o|u|y)/);
  const vowel = vm ? vm[0] : 'a';
  const cutoff = VOWEL_CUTOFF[vowel] || 900;
  const first = form.charAt(0);
  const plosive = first === 'k' || first === 't' || first === 'd' || first === 'x' || first === 'ph';
  const attack = plosive ? 0.005 : 0.06;
  const syll = Math.min(4, 1 + Math.floor(key.length / 3));
  const dur = 0.16 + 0.05 * syll;
  const type = /k$/.test(form) ? 'square' : (/(s|th)$/.test(form) ? 'triangle' : 'sine');
  return { form, freq: freq.toFixed(4), cutoff, attack, dur: dur.toFixed(4), type };
}
const tuple = p => [p.freq, p.cutoff, p.attack, p.dur, p.type].join('|');

// Hand-checked anchors: the port must reproduce these FNV-1a values by hand.
const anchors = { a: 0xe40c292c, hello: hash('hello') };
console.log('ANCHOR fnv1a("a") =', hash('a').toString(16), 'expected e40c292c', hash('a') === 0xe40c292c ? 'OK' : 'MISMATCH');
console.log('ANCHOR fnv1a("hello") =', hash('hello').toString(16));

// Corpus A: shared-lexicon bold entries plus the system dictionary.
const lexWords = new Set();
const lexDir = join(ZONE, 'builds/shared-lexicon');
for (const f of readdirSync(lexDir).filter(f => f.endsWith('.md'))) {
  const txt = readFileSync(join(lexDir, f), 'utf8');
  for (const m of txt.matchAll(/\*\*([A-Za-z]+)\*\*/g)) lexWords.add(m[1].toLowerCase());
}
const dict = existsSync('/usr/share/dict/words')
  ? readFileSync('/usr/share/dict/words', 'utf8').split('\n').map(w => w.trim()).filter(w => /^[a-z]+$/.test(w))
  : [];

// Corpus B: 10,000 pseudo-random lowercase strings, length 3 to 9, fixed seed 20261023.
const seeded = rng(20261023);
const corpusB = new Set();
while (corpusB.size < 10000) {
  const len = 3 + Math.floor(seeded() * 7);
  let s = '';
  for (let i = 0; i < len; i++) s += String.fromCharCode(97 + Math.floor(seeded() * 26));
  corpusB.add(s);
}

function report(name, words) {
  const byTuple = new Map();
  const forms = new Set();
  for (const w of words) {
    const p = paramsOf(w);
    forms.add(p.form);
    const t = tuple(p);
    if (!byTuple.has(t)) byTuple.set(t, []);
    byTuple.get(t).push(w);
  }
  let sharedWords = 0, maxGroup = 0, groupsOver1 = 0;
  for (const g of byTuple.values()) {
    if (g.length > 1) { sharedWords += g.length; groupsOver1++; }
    if (g.length > maxGroup) maxGroup = g.length;
  }
  const n = words.length;
  console.log(`\n== ${name} ==`);
  console.log(`distinct words: ${n}`);
  console.log(`distinct forms: ${forms.size}`);
  console.log(`distinct sound tuples: ${byTuple.size}`);
  console.log(`tuples shared by 2+ distinct words: ${groupsOver1}`);
  console.log(`words that share a tuple: ${sharedWords} (${(100 * sharedWords / n).toFixed(2)}%)`);
  console.log(`largest collision group: ${maxGroup}`);
  return { n, forms: forms.size, tuples: byTuple.size, sharedWords };
}

const A = [...new Set([...lexWords, ...dict])];
console.log(`\ncorpus A sources: lexicon entries=${lexWords.size}, system dictionary words=${dict.length}`);
const rA = report('Corpus A (lexicon + system dictionary, deduplicated)', A);
const rB = report('Corpus B (10,000 seeded random strings)', [...corpusB]);

console.log('\n== Verdicts against PREDICTION.md ==');
const passB = rB.tuples < rB.n && rB.forms > rB.tuples;
console.log(`PASS criterion (B): tuples<words AND forms>tuples -> ${passB ? 'PASS' : 'FAIL'}`);
console.log(`FALSIFIER (B): zero shared tuples -> ${rB.sharedWords === 0 ? 'TRIGGERED' : 'not triggered'}`);
console.log(`Corpus A is descriptive only: tuples=${rA.tuples} of words=${rA.n}`);
