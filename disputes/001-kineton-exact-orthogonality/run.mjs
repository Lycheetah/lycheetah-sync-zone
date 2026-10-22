// Dispute 001 run. Executes Kineton's REAL inline script in a stubbed DOM (no browser, no network),
// fires its real handlers, then audits the result against an exact linear-algebra projection.
// Only change to the script: before its final "})();" we append one line exposing its internals.
import fs from 'node:fs'; import vm from 'node:vm'; import path from 'node:path'; import url from 'node:url';
const here = path.dirname(url.fileURLToPath(import.meta.url));
const html = fs.readFileSync(path.join(here, '../../builds/kineton-sheaf-spectral/index.html'), 'utf8');
let src = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)][0][1];
const i = src.lastIndexOf('})();');
src = src.slice(0, i) + 'globalThis.__k={edges,faces,vertices,computeHodge};\n' + src.slice(i);

const listeners = {}; const els = {};
const noop = new Proxy(function(){}, { get: () => noop, apply: () => noop, set: () => true });
function el(id){ return els[id] ??= { id, textContent:'', value:'0.5', dataset:{}, classList:{add(){},remove(){}},
  setAttribute(){}, getContext:()=>noop, getBoundingClientRect:()=>({left:0,top:0}),
  addEventListener(t,f){ (listeners[id+':'+t] ??= []).push(f); } }; }
const win = { innerWidth:1000, innerHeight:800, devicePixelRatio:1,
  addEventListener(){}, matchMedia:()=>({matches:false,addEventListener(){}}), requestAnimationFrame(){} };
const ctx = vm.createContext({ window:win, document:{ getElementById:el, querySelectorAll:()=>[] },
  Float32Array, Math, console, setTimeout(){}, requestAnimationFrame(){}, globalThis:null });
ctx.globalThis = ctx;
vm.runInContext(src, ctx);
const K = ctx.__k, E = K.edges, F = K.faces, V = K.vertices.length;

function fire(id,t,ev){ (listeners[id+':'+t]||[]).forEach(f=>f(ev)); }
const sign = (e,f)=> ((e.u===f.u&&e.v===f.v)||(e.u===f.v&&e.v===f.w)||(e.u===f.w&&e.v===f.u))?1
                    : ((e.u===f.v&&e.v===f.u)||(e.u===f.w&&e.v===f.v)||(e.u===f.u&&e.v===f.w))?-1:0;
// ---- exact reference ----
function solve(A,b){ const n=b.length,M=A.map((r,i)=>[...r,b[i]]);
  for(let c=0;c<n;c++){ let p=c; for(let r=c+1;r<n;r++) if(Math.abs(M[r][c])>Math.abs(M[p][c])) p=r;
    [M[c],M[p]]=[M[p],M[c]]; for(let r=0;r<n;r++) if(r!==c){ const m=M[r][c]/M[c][c]; for(let k=c;k<=n;k++) M[r][k]-=m*M[c][k]; } }
  return M.map((r,i)=>r[n]/r[i]); }
const d0 = E.map(e=>{const r=Array(V).fill(0); r[e.u]=-1; r[e.v]=1; return r;});
const d1 = F.map(f=>E.map(e=>sign(e,f)));
let dd=0; for(const r of d1) for(let v=0;v<V;v++){ let s=0; E.forEach((e,j)=>s+=r[j]*d0[j][v]); dd=Math.max(dd,Math.abs(s)); }
console.log('complex check: max |d1*d0| entry =', dd, '(0 means the complex is a valid chain complex)');
function exact(w){
  const idx=[...Array(V).keys()].slice(1); // pin vertex 0
  const A=idx.map(a=>idx.map(b=>E.reduce((s,_,j)=>s+d0[j][a]*d0[j][b],0)));
  const rhs=idx.map(a=>E.reduce((s,_,j)=>s+d0[j][a]*w[j],0));
  const al=[0,...solve(A,rhs)]; const grad=E.map((_,j)=>al.reduce((s,x,v)=>s+d0[j][v]*x,0));
  const r=w.map((x,j)=>x-grad[j]);
  const B=F.map((_,a)=>F.map((_,b)=>E.reduce((s,_,j)=>s+d1[a][j]*d1[b][j],0)));
  const be=solve(B,F.map((_,a)=>E.reduce((s,_,j)=>s+d1[a][j]*r[j],0)));
  const curl=E.map((_,j)=>be.reduce((s,x,a)=>s+d1[a][j]*x,0));
  return {grad,curl,harm:w.map((x,j)=>x-grad[j]-curl[j])}; }
const dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0);

function audit(label){
  const w=E.map(e=>e.omega), g=E.map(e=>e.grad), c=E.map(e=>e.curl), h=E.map(e=>e.harm);
  const div=Array(V).fill(0); E.forEach((e,j)=>{div[e.u]-=h[j]; div[e.v]+=h[j];});
  const fc=F.map((f)=>E.reduce((s,e,j)=>s+sign(e,f)*h[j],0));
  const X=exact(w);
  const row={state:label, shownOrtho:Math.abs(dot(g,c)).toFixed(6), maxAbsDivHarm:Math.max(...div.map(Math.abs)).toFixed(6),
    maxAbsCurlComponent:Math.max(...c.map(Math.abs)).toFixed(6), maxAbsFaceCurlHarm:Math.max(...fc.map(Math.abs)).toFixed(6), harmEnergy:dot(h,h).toFixed(6),
    exactHarmEnergy:dot(X.harm,X.harm).toFixed(6), exactOrtho:Math.abs(dot(X.grad,X.curl)).toExponential(2)};
  console.log(JSON.stringify(row)); return row; }

const rows=[];
fire('startBtn','click',{}); rows.push(audit('after Witness-the-Decomposition'));
fire('circBtn','click',{}); rows.push(audit('after 1 Circulation click'));
let seed=7; const rnd=()=> (seed=(seed*16807)%2147483647)/2147483647;
for(let n=1;n<=30;n++){ // real pointerdown handler, aimed at a random edge midpoint
  const e=E[Math.floor(rnd()*E.length)], a=K.vertices[e.u], b=K.vertices[e.v];
  fire('complex','pointerdown',{clientX:(a.x+b.x)/2, clientY:(a.y+b.y)/2});
  if(n%10===0) rows.push(audit('after '+n+' edge injections')); }
const worst=Math.max(...rows.map(r=>+r.shownOrtho)), worstDiv=Math.max(...rows.map(r=>+r.maxAbsDivHarm));
console.log('\nWORST shown inner product =',worst,' (README falsifier threshold 0.05)');
console.log('WORST |div harmonic| at a vertex =',worstDiv,' (README falsifier: "non-zero divergence")');
console.log('Exact orthogonality of the true projection stays ~1e-15, so the decomposition IS orthogonal; the question is whether the 40-iteration solver reaches it.');
