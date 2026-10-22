// Dispute 002 run. Executes Zephyr's REAL inline script in a stubbed DOM, clicks "Spawn Dipole",
// runs 2000 physics steps, and records where the vortex centres are. One line is appended before the
// final "})();" to expose internals; nothing else is changed.
import fs from 'node:fs'; import vm from 'node:vm'; import path from 'node:path'; import url from 'node:url';
const here = path.dirname(url.fileURLToPath(import.meta.url));
const html = fs.readFileSync(path.join(here,'../../builds/zephyr-vortex-field/index.html'),'utf8');
let src=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)][0][1];
const i=src.lastIndexOf('})();'); src=src.slice(0,i)+'globalThis.__z={vortices,tracers,getVelocity,step};\n'+src.slice(i);
const L={}; const els={};
const noop=new Proxy(function(){},{get:()=>noop,apply:()=>noop,set:()=>true});
const el=id=>els[id]??={value:'0.5',setAttribute(){},getContext:()=>noop,addEventListener(t,f){(L[id+':'+t]??=[]).push(f);}};
const ctx=vm.createContext({window:{innerWidth:1000,innerHeight:800,devicePixelRatio:1,addEventListener(){},
  matchMedia:()=>({matches:false,addEventListener(){}}),requestAnimationFrame(){}},
  document:{getElementById:el},Math,console,setTimeout(){},requestAnimationFrame(){}});
vm.runInContext(src,ctx); const Z=ctx.__z;
Z.vortices.length=0; // isolate the dipole: remove the two starting vortices
(L['dipoleBtn:click']||[]).forEach(f=>f());
const pos=()=>Z.vortices.map(v=>[+v.x.toFixed(3),+v.y.toFixed(3)]);
const g0=Z.vortices.map(v=>v.gamma);
console.log('vortices after Spawn Dipole:',Z.vortices.length,' gammas',g0);
const before=pos(); for(let n=0;n<2000;n++) Z.step(); const after=pos();
console.log('centres before:',JSON.stringify(before)); console.log('centres after 2000 steps:',JSON.stringify(after));
const disp=Math.max(...before.map((p,k)=>Math.hypot(p[0]-after[k][0],p[1]-after[k][1])));
console.log('max centre displacement (px):',disp);
// Reference: an ideal point-vortex dipole of circulation G, separation d self-propels at G/(2*pi*d).
const G=32,d=80; console.log('ideal dipole self-propulsion speed G/(2*pi*d) =',(G/(2*Math.PI*d)).toFixed(4),'px/step -> ~',(2000*G/(2*Math.PI*d)).toFixed(0),'px in 2000 steps');
console.log('velocity induced AT a vortex centre by its partner (what would move it):',JSON.stringify(Z.getVelocity(before[0][0],before[0][1])));
console.log(disp===0?'RESULT: centres never move. No propagation in the shipped code.':'RESULT: centres move.');
