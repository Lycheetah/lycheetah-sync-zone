#!/usr/bin/env node
// Stub-DOM check for builds/wren-stairwell (round four).
// NOT a browser: nothing is rendered, no GPU, no real layout. It runs the page's
// inline script against a small fake DOM and records canvas calls.
// Usage: node stub-check.mjs [path/to/index.html]
// Exit: 0 when every check passes, 1 on any failure.

import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const file = process.argv[2] || path.join(here, 'index.html');
const html = fs.readFileSync(file, 'utf8');
const m = html.match(/<script>([\s\S]*?)<\/script>/);
if (!m) { console.error('no inline script in ' + file); process.exit(2); }
const SRC = m[1];
const CAPTION = 'The stairs are drawn on paper instead.';

const DRAW_OPS = ['fillRect', 'strokeRect', 'fillText', 'beginPath', 'arc', 'fill', 'stroke',
  'moveTo', 'lineTo', 'setTransform', 'clearRect', 'save', 'restore', 'drawImage'];

// A fake world. `opts.webgl` says whether getContext('webgl') can succeed;
// `opts.compileFail` makes the shader compile report failure.
function makeWorld(opts) {
  const log = [];
  const win = {
    innerWidth: opts.w, innerHeight: opts.h, listeners: {},
    addEventListener(t, f) { (this.listeners[t] ||= []).push(f); },
    matchMedia: () => ({ matches: false }),
    requestAnimationFrame: () => 0,
  };

  function glStub() {
    const gl = {
      VERTEX_SHADER: 35633, FRAGMENT_SHADER: 35632, COMPILE_STATUS: 35713, LINK_STATUS: 35714,
      ARRAY_BUFFER: 34962, STATIC_DRAW: 35044, FLOAT: 5126, TRIANGLES: 4,
      createShader: () => ({}), shaderSource() {}, compileShader() {},
      getShaderParameter: () => !opts.compileFail,
      getShaderInfoLog: () => 'stub: forced compile failure',
      deleteShader() {}, createProgram: () => ({}), attachShader() {}, linkProgram() {},
      getProgramParameter: () => true, getProgramInfoLog: () => '', useProgram() {},
      createBuffer: () => ({}), bindBuffer() {}, bufferData() {}, getAttribLocation: () => 0,
      enableVertexAttribArray() {}, vertexAttribPointer() {}, getUniformLocation: () => ({}),
      viewport() {}, uniform1f() {}, uniform2f() {}, uniform3f() {}, drawArrays() {},
    };
    return gl;
  }

  function ctx2d(canvas) {
    const c = { fillStyle: '', strokeStyle: '', font: '', textAlign: '', lineWidth: 1,
      globalAlpha: 1, lineCap: '', lineJoin: '' };
    for (const name of DRAW_OPS) {
      c[name] = (...args) => { log.push({ op: name, canvas, args }); };
    }
    c.createRadialGradient = () => ({ addColorStop() {} });
    c.createLinearGradient = () => ({ addColorStop() {} });
    return c;
  }

  function makeCanvas(id) {
    const c = {
      id, kind: null, attrs: {}, parentNode: null, _w: 300, _h: 150,
      get width() { return this._w; },
      set width(v) { this._w = v; log.push({ op: 'width', canvas: this, args: [v] }); },
      get height() { return this._h; },
      set height(v) { this._h = v; },
      setAttribute(k, v) { this.attrs[k] = v; }, getAttribute(k) { return this.attrs[k] ?? null; },
      focus() {}, addEventListener() {},
      // Like a browser: a canvas keeps the first context type it was given.
      cloneNode() { return makeCanvas(id); },
      getContext(kind) {
        if (this.kind && this.kind !== (kind === 'experimental-webgl' ? 'webgl' : kind)) return null;
        if (kind === '2d') { this.kind = '2d'; return ctx2d(this); }
        if (kind === 'webgl' || kind === 'experimental-webgl') {
          if (!opts.webgl) return null;
          this.kind = 'webgl';
          return glStub();
        }
        return null;
      },
    };
    return c;
  }

  const doc = {
    world: null,
    els: {},
    getElementById(id) {
      if (id === 'world') return doc.world;
      return (doc.els[id] ||= { id, textContent: '', disabled: false, attrs: {},
        setAttribute(k, v) { this.attrs[k] = v; }, addEventListener() {} });
    },
  };
  doc.world = makeCanvas('world');
  doc.world.parentNode = {
    replaceChild(n, o) { doc.world = n; n.parentNode = o.parentNode; return o; },
  };

  return { log, win, doc };
}

function run(opts) {
  const world = makeWorld(opts);
  const original = world.doc.world;
  const sandbox = {
    document: world.doc, window: world.win, console,
    performance: { now: () => 0 }, matchMedia: world.win.matchMedia,
    requestAnimationFrame: world.win.requestAnimationFrame,
  };
  vm.createContext(sandbox);
  vm.runInContext(SRC, sandbox, { filename: 'inline-script' });
  return { ...world, original };
}

function fireResize(world, w, h) {
  world.win.innerWidth = w;
  world.win.innerHeight = h;
  for (const f of world.win.listeners.resize || []) f({});
}

function captionDrawnAfter(world, from, canvas) {
  return world.log.slice(from).some(e =>
    e.op === 'fillText' && e.canvas === canvas && String(e.args[0]).includes(CAPTION));
}

const results = [];
function check(name, ok, detail) { results.push({ name, ok, detail }); }

// W1: no WebGL. Fallback is drawn at 390x844, then the device rotates to 844x390.
{
  const world = run({ w: 390, h: 844, webgl: false, compileFail: false });
  const visible = world.doc.world;
  const first = captionDrawnAfter(world, 0, visible);
  check('W1 fallback caption drawn at load (no WebGL)', first, `visible canvas ${visible.width}x${visible.height}`);
  const mark = world.log.length;
  fireResize(world, 844, 390);
  const redrawn = captionDrawnAfter(world, mark, world.doc.world);
  check('W1 caption redrawn after rotation (no WebGL)', redrawn,
    `visible canvas after resize: ${world.doc.world.width}x${world.doc.world.height}, new draw ops: ${world.log.length - mark}`);
  check('W1 canvas matches rotated viewport', world.doc.world.width === 844 && world.doc.world.height === 390,
    `width ${world.doc.world.width}, height ${world.doc.world.height}`);
}

// W2: WebGL context bound, shader fails, fallback must clone the canvas. Then resize.
{
  const world = run({ w: 390, h: 844, webgl: true, compileFail: true });
  const visible = world.doc.world;
  check('W2 clone branch swapped the visible canvas', visible !== world.original,
    visible === world.original ? 'no clone happened' : 'clone is in the document');
  check('W2 caption drawn on the cloned canvas', captionDrawnAfter(world, 0, visible), '');
  fireResize(world, 844, 390);
  check('W2 resize reaches the visible canvas', world.doc.world.width === 844 && world.doc.world.height === 390,
    `visible ${world.doc.world.width}x${world.doc.world.height}; original detached canvas ${world.original.width}x${world.original.height}`);
}

let failed = 0;
console.log(`stub-check ${path.basename(file)} (stub DOM, not a browser)`);
for (const r of results) {
  if (!r.ok) failed++;
  console.log(`${r.ok ? 'PASS' : 'FAIL'}  ${r.name}${r.detail ? '  [' + r.detail + ']' : ''}`);
}
console.log(failed ? `${failed} check(s) failed` : 'all checks passed');
process.exit(failed ? 1 : 0);
