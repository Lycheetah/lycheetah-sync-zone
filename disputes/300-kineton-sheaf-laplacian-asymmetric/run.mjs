// Rebuilds the update rule of builds/kineton-sheaf-automata/index.html (lines 183-267) verbatim
// and tests whether the implemented operator is a sheaf Laplacian delta*delta (symmetric, PSD).
const COLS=24,ROWS=16,N=COLS*ROWS;
const idx=(c,r)=>(c<0||c>=COLS||r<0||r>=ROWS)?-1:r*COLS+c;
const nb=[];for(let r=0;r<ROWS;r++)for(let c=0;c<COLS;c++){const odd=c%2;
 const off=odd?[[0,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0]]:[[0,-1],[1,-1],[1,0],[0,1],[-1,0],[-1,-1]];
 nb.push(off.map(o=>idx(c+o[0],r+o[1])).filter(i=>i>=0));}
const col=i=>i%COLS;
function Lmat(th){const n=2*N,L=Array.from({length:n},()=>new Float64Array(n));const ct=Math.cos(th),st=Math.sin(th);
 for(let i=0;i<N;i++)for(const j of nb[i]){const rot=col(j)>col(i);
  // lap_i += x_i - M x_j, M = R_theta if nbr col > cell col else identity
  L[2*i][2*i]+=1;L[2*i+1][2*i+1]+=1;
  if(rot){L[2*i][2*j]-=ct;L[2*i][2*j+1]+=st;L[2*i+1][2*j]-=st;L[2*i+1][2*j+1]-=ct;}
  else{L[2*i][2*j]-=1;L[2*i+1][2*j+1]-=1;}}
 return L;}
for(const th of [0,Math.PI/3]){const L=Lmat(th);let asym=0;
 for(let a=0;a<2*N;a++)for(let b=0;b<a;b++)asym=Math.max(asym,Math.abs(L[a][b]-L[b][a]));
 console.log('theta=',th.toFixed(3),'max |L - L^T| =',asym.toFixed(4));}
// boundedness: soliton amplitude 1.2 injected as in the page, run 3000 steps at theta=pi/3
function sim(th,steps){const u=new Float64Array(N),v=new Float64Array(N);
 for(let i=0;i<N;i++){u[i]=(Math.random()-.5)*.4;v[i]=(Math.random()-.5)*.4;}
 for(let i=0;i<N;i++){const dx=col(i)-12,dy=Math.floor(i/COLS)-8,d=Math.hypot(dx,dy);if(d<6&&d>.1){const a=Math.atan2(dy,dx)+Math.PI/2;u[i]=Math.cos(a)*1.2;v[i]=Math.sin(a)*1.2;}}
 const ct=Math.cos(th),st=Math.sin(th);let mx=0;
 for(let s=0;s<steps;s++){const nu=new Float64Array(N),nv=new Float64Array(N);
  for(let i=0;i<N;i++){let lu=0,lv=0;for(const j of nb[i]){let a=u[j],b=v[j];if(col(j)>col(i)){[a,b]=[a*ct-b*st,a*st+b*ct];}lu+=u[i]-a;lv+=v[i]-b;}
   const m2=u[i]**2+v[i]**2;nu[i]=u[i]-.12*lu+.04*u[i]*(1-m2);nv[i]=v[i]-.12*lv+.04*v[i]*(1-m2);}
  u.set(nu);v.set(nv);for(let i=0;i<N;i++)mx=Math.max(mx,Math.hypot(u[i],v[i]));}
 return mx;}
for(const th of [0,Math.PI/3,Math.PI]){console.log('theta',th.toFixed(3),'max |x| over 3000 steps =',sim(th,3000).toFixed(4));}
