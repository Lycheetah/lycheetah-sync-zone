// Dispute 200 run. Executes Aetheron's REAL inline script in a stubbed DOM (no browser, no network),
// then measures total potential sum(phi) across stepLaplacian() at the shipped default damping and at damping = 1.0.
// Only change to the script: before its final "})();" we append one line exposing internals.
import fs from 'node:fs'; import vm from 'node:vm'; import path from 'node:path'; import url from 'node:url';
const here = path.dirname(url.fileURLToPath(import.meta.url));
const html = fs.readFileSync(path.join(here, '../../builds/aetheron-spectral-loom/index.html'), 'utf8');
let src = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].pop()[1];
const i = src.lastIndexOf('})();');
src = src.slice(0, i) + 'globalThis.__a={nodes,edges,stepLaplacian};\n' + src.slice(i);
const listeners = {}; const els = {};
const noop = new Proxy(function(){}, { get: () => noop, apply: () => noop, set: () => true });
function el(id){ return els[id] ??= { id, textContent:'', value:'0.5', dataset:{}, style:{}, classList:{add(){},remove(){},toggle(){}},
  setAttribute(){}, getContext:()=>noop, getBoundingClientRect:()=>({left:0,top:0,width:1000,height:800}),
  addEventListener(t,f){ (listeners[id+':'+t] ??= []).push(f); } }; }
const win = { innerWidth:1000, innerHeight:800, devicePixelRatio:1,
  addEventListener(){}, matchMedia:()=>({matches:false,addEventListener(){}}), requestAnimationFrame(){} };
const ctx = vm.createContext({ window:win, document:{ getElementById:el, querySelectorAll:()=>[], addEventListener(){}, body:el('body') },
  Float32Array, Math, console, setTimeout(){}, requestAnimationFrame(){}, performance:{now:()=>0}, globalThis:null });
ctx.globalThis = ctx;
vm.runInContext(src, ctx);
const A = ctx.__a;
const total = () => A.nodes.reduce((s, n) => s + n.phi, 0);
function trial(label, damp) {
  A.nodes.forEach((n, k) => { n.phi = (k % 3 === 0) ? 0.8 : 0.1; });
  if (damp !== null) { el('damp').value = String(damp); (listeners['damp:input'] || []).forEach(f => f({})); }
  const t0 = total(); const out = [];
  for (let s = 1; s <= 200; s++) { A.stepLaplacian(); if (s === 1 || s === 50 || s === 200) out.push(`step ${s}: ${total().toFixed(6)}`); }
  console.log(`${label}: sum(phi) start ${t0.toFixed(6)} | ${out.join(' | ')} | retained ${(100 * total() / t0).toFixed(2)}%`);
  return total() / t0;
}
const rDefault = trial('shipped default (damping 0.985, no slider touched)', null);
const rOne = trial('slider set to 1.000 ("Pure Conservation")', 1.0);
console.log(`\nREADME claim: total potential "strictly conserved" "under pure diffusion without damping".`);
console.log(`Default run retains ${(100 * rDefault).toFixed(2)}% after 200 steps; damping=1.0 retains ${(100 * rOne).toFixed(6)}%.`);
console.log(rDefault < 0.5 && Math.abs(rOne - 1) < 1e-4 ? 'MEASURED: conserved only at damping 1.0; the shipped default dissipates.' : 'UNEXPECTED');
