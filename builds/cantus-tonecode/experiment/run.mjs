// Cantus, round five. Reuses Plumb's corpus method (experiments/plumb-tone-injectivity/run.mjs):
// same rng, same seed 20261023, same lexicon bold-word regex, same dictionary filter.
// Core code is extracted from ../index.html between CORE-BEGIN/CORE-END (single source of truth).
import { readFileSync, readdirSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
const here = dirname(fileURLToPath(import.meta.url));
const ZONE = join(here, '../../..');
const html = readFileSync(join(here, '../index.html'), 'utf8');
const src = html.split('/*CORE-BEGIN*/')[1].split('/*CORE-END*/')[0];
const load = s => new Function(s + '; return {CB,IDX,encode,decode,grammar};')();
const S = load(src);
function rng(seed){let a=seed>>>0;return()=>{a=(a+0x6D2B79F5)>>>0;let t=a;t=Math.imul(t^(t>>>15),t|1);t^=t+Math.imul(t^(t>>>7),t|61);return((t^(t>>>14))>>>0)/4294967296;};}
const lex=new Set(),dir=join(ZONE,'builds/shared-lexicon');
for(const f of readdirSync(dir).filter(f=>f.endsWith('.md')))for(const m of readFileSync(join(dir,f),'utf8').matchAll(/\*\*([A-Za-z]+)\*\*/g))lex.add(m[1].toLowerCase());
const dict=readFileSync('/usr/share/dict/words','utf8').split('\n').map(w=>w.trim()).filter(w=>/^[a-z]+$/.test(w));
const r=rng(20261023),B=new Set();
while(B.size<10000){const n=3+Math.floor(r()*7);let s='';for(let i=0;i<n;i++)s+=String.fromCharCode(97+Math.floor(r()*26));B.add(s);}
const A=[...new Set([...lex,...dict])];
function roundtrip(name,words,API){
  let bad=0,tones=0,seen=new Map(),coll=0,first=null;
  for(const w of words){const e=API.encode(w),d=API.decode(e.tones);tones+=e.tones.length;
    if(e.errors.length||d.error||d.text!==w){bad++;if(!first)first=[w,d.text];}
    const k=e.tones.join('');if(seen.has(k)&&seen.get(k)!==w)coll++;else seen.set(k,w);}
  console.log(`${name}: words=${words.length} roundtrip_failures=${bad} tone_collisions=${coll} mean_tones=${(tones/words.length).toFixed(2)} acc=${(100*(words.length-bad)/words.length).toFixed(3)}%`+(first?` first_fail=${JSON.stringify(first)}`:''));
  return bad+coll;
}
let fails=0;
console.log('== Cantus round-trip (single words) ==');
fails+=roundtrip('A lexicon+dictionary',A,S);fails+=roundtrip('B random strings',[...B],S);
const unassigned=[...lex].filter(w=>S.IDX[w]===undefined);
console.log(`lexicon words: ${lex.size}; without a short codeword (spelled instead): ${unassigned.length} ${JSON.stringify(unassigned)}`);
console.log('lexicon words at 3 tones:',[...lex].filter(w=>S.IDX[w]!==undefined).every(w=>S.encode(w).tones.length===3));

console.log('== random sentences ==');
const r2=rng(7),pool=S.CB.map(e=>e[0]).filter(w=>w[0]!=='-'),sfx=S.CB.map(e=>e[0]).filter(w=>w[0]==='-'),Bl=[...B];
let sb=0;for(let i=0;i<5000;i++){const n=1+Math.floor(r2()*8);const toks=[];
  for(let j=0;j<n;j++){let w=r2()<.5?pool[Math.floor(r2()*pool.length)]:Bl[Math.floor(r2()*Bl.length)];
    if(!/^[.?]$/.test(w)&&r2()<.2)w+=sfx[Math.floor(r2()*sfx.length)];toks.push(w);}
  const canon=S.decode(S.encode(toks.join(' ')).tones).text; // canonical form of the typed tokens
  const again=S.decode(S.encode(canon).tones);
  const direct=S.encode(toks.join(' ')).tones.join(',')===S.encode(canon).tones.join(',');
  if(again.text!==canon||again.error||!direct)sb++;}
console.log(`sentences=5000 failures=${sb}`);fails+=sb;

console.log('== exhaustive tone sequences, length 1..8 ==');
let total=0,valid=0,cx=0;const seq=[];
(function rec(len){if(len>0){total++;const d=S.decode(seq);if(!d.error){valid++;const e=S.encode(d.text);if(e.errors.length||e.tones.join()!==seq.join())cx++;}}
  if(len===8)return;for(let t=0;t<6;t++){seq.push(t);rec(len+1);seq.pop();}})(0);
console.log(`sequences=${total} decodable=${valid} counterexamples=${cx}`);fails+=cx;

console.log('== mutant (END pair 35 -> 34) must fail ==');
const M=load(src.replace('var END=35','var END=34'));
const mf=A.filter(w=>{const d=M.decode(M.encode(w).tones);return d.error||d.text!==w;}).length;
console.log(`mutant roundtrip failures on corpus A: ${mf} -> ${mf>0?'check CAN fail (good)':'CHECK CANNOT FAIL (bad)'}`);

console.log('== examples parse as grammatical ==');
const ex=[...html.matchAll(/\['([^']+ [.?])','[^']+'\]/g)].map(m=>m[1]);
let ng=0;for(const e of ex){const g=S.grammar(S.decode(S.encode(e).tones).tokens);const ok=g.every(s=>s.ok);if(!ok)ng++;console.log(ok?'ok  ':'FAIL',e);}
console.log(`examples=${ex.length} not_grammatical=${ng}`);fails+=ng;

console.log('== against Plumb (Mycel mapping), secondary ==');
const pl=spawnSync('node',[join(ZONE,'experiments/plumb-tone-injectivity/run.mjs')],{encoding:'utf8'});
for(const l of pl.stdout.split('\n').filter(l=>/distinct sound tuples|== Corpus/.test(l)))console.log('plumb:',l);
// Mycel mapping on the lexicon alone (port of paramsOf from Plumb's run.mjs, which ports Mycel's index.html)
const t=readFileSync(join(ZONE,'experiments/plumb-tone-injectivity/run.mjs'),'utf8');
const body=t.split("const ZONE")[0]+t.slice(t.indexOf('const CONS'),t.indexOf('// Hand-checked anchors'));
const P=new Function(body.replace(/import[^\n]*\n/g,'')+';return {paramsOf,tuple,rng};')();
const lt=new Map();for(const w of lex){const k=P.tuple(P.paramsOf(w));lt.set(k,(lt.get(k)||[]).concat(w));}
console.log(`Mycel mapping on the ${lex.size} lexicon words alone: distinct tuples=${lt.size}, colliding groups=${[...lt.values()].filter(g=>g.length>1).length}`);
console.log(`pigeonhole minimum sharing for 63896 words in 3300 tuples: ${(100*(63896-3300)/63896).toFixed(2)}%`);
// birthday: words until first tuple collision, 200 trials of random strings
const r3=rng(99),firsts=[];for(let k=0;k<200;k++){const s=new Set();let n=0;for(;;){n++;let w='';const L=3+Math.floor(r3()*7);for(let i=0;i<L;i++)w+=String.fromCharCode(97+Math.floor(r3()*26));const q=P.tuple(P.paramsOf(w));if(s.has(q))break;s.add(q);}firsts.push(n);}
firsts.sort((a,b)=>a-b);console.log(`random words until first Mycel tuple collision: median=${firsts[100]} min=${firsts[0]} max=${firsts[199]}`);
console.log(`\nTOTAL FAILURES against predictions 1-3,6-examples: ${fails}`);
process.exit(0);
