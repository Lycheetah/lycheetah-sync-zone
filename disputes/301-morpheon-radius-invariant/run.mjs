// builds/morpheon-latent-weaver/index.html lines 432-452: r1=r2=0.65, r3=0.38, x5=r3*sin(u+v).
const r1=.65,r2=.65,r3=.38;let lo=9,hi=0;
for(let u=0;u<6.2832;u+=.01)for(let v=0;v<6.2832;v+=.01){const s=Math.sin(u+v);const R=Math.sqrt(r1*r1+r2*r2+(r3*s)**2);lo=Math.min(lo,R);hi=Math.max(hi,R);}
console.log('5D radius over the embedded torus: min',lo.toFixed(4),'max',hi.toFixed(4));
console.log('constant (invariant)?',Math.abs(hi-lo)<1e-9,'| lies ON unit S^4?',Math.abs(hi-1)<1e-9&&Math.abs(lo-1)<1e-9);
