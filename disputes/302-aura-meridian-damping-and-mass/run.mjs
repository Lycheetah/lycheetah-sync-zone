import fs from 'node:fs';
const h=fs.readFileSync(new URL('../../builds/aura-meridian-standing-wave/index.html',import.meta.url),'utf8');
const r=fs.readFileSync(new URL('../../builds/aura-meridian-standing-wave/README.md',import.meta.url),'utf8');
console.log('README claims a Damping control:',/Damping \(\$\\gamma\$\)/.test(r));
console.log('page has a damping/gamma input:',/id="(damp|gamma)/i.test(h),'| any "damp" in page source:',/damp/i.test(h.replace(/<style[\s\S]*?<\/style>/,'')));
console.log('README claims integral|Psi|^2 = 1.0 +- 1e-5; page computes an integral/norm:',/trapz|integral|norm|sum\s*\+=/i.test(h.split('<script>')[1]));
console.log('csolVal element written by script:',(h.split('<script>')[1].match(/csolVal/g)||[]).length>0,'(0 = static label)');
