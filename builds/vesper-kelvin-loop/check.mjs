// Headless measurement of the Kelvin Loop core (the same code the page runs).
import fs from 'node:fs';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
const dir=path.dirname(fileURLToPath(import.meta.url));
const html=fs.readFileSync(path.join(dir,'index.html'),'utf8');
const src=html.split('/*<CORE>*/')[1].split('/*</CORE>*/')[0];
const createCore=new Function(src+'\nreturn createCore;')();
const out=[];const P=s=>{out.push(s);console.log(s);};
const names=['loopGamma','H','sumGx','sumGy','sumGr2'];
function scene(o){const c=createCore(o);c.vort=[{x:-0.28,y:0,g:1.5},{x:0.28,y:0,g:1.5}];if(o&&o.third)c.vort.push({x:2.1,y:0.15,g:-1.5});c.setRing(0,0,1.0,160);c.rebase();return c;}
function run(label,o,N,dt,setup){
  const c=scene(o);if(setup)setup(c);const mx=[0,0,0,0,0];let g0=c.sg;
  for(let i=0;i<N;i++){c.step(dt);if(i%50===0||i===N-1){const r=c.drift().rel;for(let k=0;k<5;k++)mx[k]=Math.max(mx[k],Math.abs(r[k]));}}
  const d=c.drift();
  P(`${label.padEnd(34)} T=${(N*dt).toFixed(0).padStart(3)}  max|rel drift|: `+names.map((n,k)=>`${n} ${mx[k].toExponential(1)}`).join('  ')+`  | loop pts ${c.lx.length}, nearest core ${c.closest().toFixed(2)}sigma, sum|G| ${c.vort.reduce((a,v)=>a+Math.abs(v.g),0).toFixed(4)}`);
  return {mx,c};
}
P('Kelvin Loop check, node '+process.version+', sigma=0.15, scene: +1.5,+1.5 pair ringed by material loop R=1.0 (third=-1.5 vortex at (2.1,0.15) where stated)');
P('relative drift scales: loopGamma/max(|G0|,0.1*sum|G|), H/(0.05*sum|G|^2), P/sum|G|, I/sum|G|. A = ideal Euler dynamics.');
P('');
P('A. ideal (free vortices, RK4, no viscosity), dt convergence');
const a1=run('A1 dt=0.01',{}, 2000,0.01);
const a2=run('A2 dt=0.005',{},4000,0.005);
const a3=run('A3 dt=0.0025',{},8000,0.0025);
P('  H drift ratio dt 0.01 / 0.005 = '+(a1.mx[1]/a2.mx[1]).toFixed(1)+' ; 0.005 / 0.0025 = '+(a2.mx[1]/a3.mx[1]).toFixed(1)+'  (RK4 would be ~16)');
P('');P('B. same, forward Euler stepper');
run('B1 Euler dt=0.005',{rk4:false},4000,0.005);
P('');P('A-stress. the pair plus a -1.5 vortex (strong strain; loop filaments past the 6000-point cap)');
run('A4 third vortex, RK4 dt=0.005',{third:true},4000,0.005);
P('');P('C. Zephyr earlier version (frozen vortices) + stepper + decay: frozen, Euler, viscosity 0.9995/frame');
const cz=run('C1 frozen+Euler+viscous dt=1/180',{move:false,rk4:false,decay:true},180*20,1/180);
{const c=scene({move:false,rk4:false,decay:true});let f=0;while(c.vort[0].g>0.75){c.step(1/60);f++;}P(`  frames (60/s) until circulation halves: ${f} (analytic ln2/-ln0.9995 = ${(Math.log(2)/-Math.log(0.9995)).toFixed(0)}) = ${(f/60).toFixed(1)} s`);}
P('');P('D. frozen vortices, no viscosity (Zephyr geometry, honest integrator)');
run('D1 frozen+RK4',{move:false,decay:false},4000,0.005);
run('D2 frozen+Euler',{move:false,rk4:false,decay:false},4000,0.005);
P('');P('E. loop that cuts through a core (ring R=0.28 centred on a vortex, sigma=0.15)');
run('E1 free+RK4, loop cuts core',{},2000,0.005,c=>{c.setRing(-0.28,0,0.15,120);c.rebase();});
P('');P('F. dipole speed: +1.5/-1.5 separation d=0.6, theory U = G(1-exp(-d^2/s^2))/(2 pi d)');
{const c=createCore({});c.vort=[{x:0,y:0.3,g:1.5},{x:0,y:-0.3,g:-1.5}];c.lx=[];c.ly=[];c.rebase();for(let i=0;i<4000;i++)c.step(0.005);
 const d=0.6,U=1.5*(1-Math.exp(-d*d/0.0225))/(2*Math.PI*d);const meas=Math.abs(c.vort[0].x)/(4000*0.005);P(`  measured ${meas.toFixed(5)}  theory ${U.toFixed(5)}  rel err ${(Math.abs(meas-U)/U).toExponential(1)}`);}
P('');P('G. Zephyr source (read only, file as it is on disk now: builds/zephyr-vortex-field/index.html)');
{const z=fs.readFileSync(path.join(dir,'..','zephyr-vortex-field','index.html'),'utf8');
 const posWrites=(z.match(/vortices\[[^\]]*\]\.(x|y)\s*[+\-]?=(?!=)/g)||[]).length;
 const gw=(z.match(/\.gamma\s*\*=\s*[0-9.]+/g)||[]);
 P(`  vortex x/y write statements: ${posWrites} (their vortices DO move in this version; my first read of it, earlier today, had none)`);
 P(`  gamma multipliers (decay/settle): ${gw.join(' , ')}`);
 P(`  integrator: forward Euler, dt = 1 frame, in px/frame: ${/x \+= vVel\[vi\]\.u/.test(z)}`);}
P('');P('H. Their pairwise law (Gamma=28, core=35 px, as in their file) run through MY core at dt=1 frame, co-rotating pair d=100 px');
P('   (my kernel omits their +0.1 px softening: a reimplementation, not their file. Euler = their stepper; RK4 = same law, honest stepper)');
for(const [nm,rk] of [['Euler (theirs)',false],['RK4',true]]){
  const c=createCore({sigma:35,rk4:rk,refine:0});c.vort=[{x:-50,y:0,g:28},{x:50,y:0,g:28}];c.rebase();
  const s0=Math.hypot(c.vort[1].x-c.vort[0].x,c.vort[1].y-c.vort[0].y);const rows=[];
  for(let f=1;f<=3600;f++){c.step(1);if(f===600||f===1800||f===3600){const s=Math.hypot(c.vort[1].x-c.vort[0].x,c.vort[1].y-c.vort[0].y);rows.push(`f${f}: sep ${(s/s0).toFixed(4)}x  H ${c.drift().rel[1].toExponential(1)}`);}}
  P(`  ${nm.padEnd(15)} `+rows.join(' | '));}
fs.writeFileSync(path.join(dir,'RESULT.txt'),out.join('\n')+'\n');
