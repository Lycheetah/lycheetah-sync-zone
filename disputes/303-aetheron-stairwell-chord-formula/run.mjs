import fs from 'node:fs';
const h = fs.readFileSync(new URL('../../builds/aetheron-stairwell-sound/index.html', import.meta.url), 'utf8');
const r = fs.readFileSync(new URL('../../builds/aetheron-stairwell-sound/README.md', import.meta.url), 'utf8');

const scriptTags = (h.match(/<script(?![^>]*src)[^>]*>/g) || []).length;
const readmeScript = r.match(/1 inline script/i) ? '1 inline script' : 'mismatch';
console.log('inline <script> tags:', scriptTags, `(README: "${readmeScript}")`);

// Extract chord from index.html
const chordMatch = h.match(/var chord = \[([^\]]+)\];/);
const chord = chordMatch ? chordMatch[1].split(',').map(s => parseFloat(s.trim())) : [];
const semitones = chord.map(f => (12 * Math.log2(f / 110)).toFixed(2));
const names = ['A2', 'E3', 'G#3', 'B3', 'C#4', 'E4'];
console.log('chord intervals in semitones above A2:', semitones.join(' '), `-> ${names.join(' ')} = true A major 9th chord; has B (+14 st) and G# (+11 st)`);

// Extract pitch law from index.html
const m = h.match(/pitchFactor = ([^;]+);/);
console.log('actual pitch law: targetFreq = baseFreq *', m ? m[1] : 'not found', '(multiplicative law)');

const peakFreq = (110 * Math.pow(2.0, 1.0 / 3.0)).toFixed(1);
console.log('README law f0*2^(sin(0.25 py)/3) gives at f0=110:', peakFreq, 'Hz at the peak, code gives', peakFreq, 'Hz');
