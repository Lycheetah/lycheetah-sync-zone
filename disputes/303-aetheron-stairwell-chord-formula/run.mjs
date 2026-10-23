import fs from 'node:fs';
const h=fs.readFileSync(new URL('../../builds/aetheron-stairwell-sound/index.html',import.meta.url),'utf8');
console.log('inline <script> tags:',(h.match(/<script(?![^>]*src)[^>]*>/g)||[]).length,'(README: "0 scripts")');
const chord=[110.0,164.81,220.0,277.18,329.63];
console.log('chord intervals in semitones above A2:',chord.map(f=>(12*Math.log2(f/110)).toFixed(2)).join(' '),'-> A E A C# E = A major triad; a major 9 needs B (+14 st) and has none');
const m=h.match(/heightPitchShift = ([^;]+);/);console.log('actual pitch law:',m[1],'added to base frequency (additive +-8 Hz, includes a time term)');
console.log('README law f0*2^(sin(0.25 py)/3) would give at f0=110:',(110*2**(1/3)).toFixed(1),'Hz at the peak, code gives',(110+8).toFixed(1));
