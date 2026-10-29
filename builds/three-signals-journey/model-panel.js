(() => {
  "use strict";

  const TAU = 2 * Math.PI;
  const SVG_NS = "http://www.w3.org/2000/svg";
  const Q_BY_TAIL = Object.freeze({ ra: 2, le: 5, hu: 7 });
  const REFERENCE_DELTA = 0.5;

  function makeElement(tagName, className, text) {
    const element = document.createElement(tagName);
    if (className) element.className = className;
    if (text !== undefined) element.textContent = text;
    return element;
  }

  function makeSvgElement(tagName, className, attributes, text) {
    const element = document.createElementNS(SVG_NS, tagName);
    if (className) element.setAttribute("class", className);
    Object.entries(attributes || {}).forEach(([name, value]) => {
      element.setAttribute(name, String(value));
    });
    if (text !== undefined) element.textContent = text;
    return element;
  }

  function wrap(angle) {
    const remainder = angle % TAU;
    return remainder < 0 ? remainder + TAU : remainder;
  }

  function distanceToZero(phase) {
    return Math.min(phase, TAU - phase);
  }

  function formatRadians(value) {
    return `${value.toFixed(3)} rad`;
  }

  function phasePoint(cx, cy, radius, phase) {
    return {
      x: cx + radius * Math.cos(phase),
      y: cy - radius * Math.sin(phase)
    };
  }

  function makePhaseDialFigure(q, theta1, theta2) {
    const figure = makeElement("figure", "model-panel__phase-figure");
    const caption = makeElement(
      "figcaption",
      "model-panel__phase-caption",
      "Current ideal phases · zero points right; positive angles turn counterclockwise."
    );
    const svg = makeSvgElement("svg", "model-panel__phase-svg", {
      viewBox: "0 0 360 180",
      width: "360",
      height: "180",
      role: "img",
      "aria-labelledby": "model-panel-dials-title model-panel-dials-description",
      focusable: "false"
    });
    svg.style.display = "block";
    svg.style.width = "min(100%, 360px)";
    svg.style.maxWidth = "100%";
    svg.style.height = "auto";

    const title = makeSvgElement(
      "title",
      "",
      { id: "model-panel-dials-title" },
      "Two labeled dials for the current ideal phase state"
    );
    const description = makeSvgElement(
      "desc",
      "",
      { id: "model-panel-dials-description" },
      `For q = ${q}, theta1 is ${formatRadians(theta1)} and theta2 is ${formatRadians(theta2)}. Zero is at the right of each dial; positive phase is counterclockwise.`
    );
    svg.append(title, description);

    [
      { cx: 100, phase: theta1, label: "theta1", value: formatRadians(theta1), handClass: "model-panel__dial-hand--one" },
      { cx: 260, phase: theta2, label: "theta2", value: formatRadians(theta2), handClass: "model-panel__dial-hand--two" }
    ].forEach((dial) => {
      const cy = 66;
      const ringRadius = 47;
      const group = makeSvgElement("g", "model-panel__dial", {});
      group.append(makeSvgElement("circle", "model-panel__dial-ring", {
        cx: dial.cx,
        cy,
        r: ringRadius,
        fill: "none",
        stroke: "currentColor",
        "stroke-opacity": "0.55",
        "stroke-width": "1.5"
      }));

      [0, Math.PI / 2, Math.PI, 3 * Math.PI / 2].forEach((angle) => {
        const start = phasePoint(dial.cx, cy, ringRadius - 5, angle);
        const end = phasePoint(dial.cx, cy, ringRadius, angle);
        group.append(makeSvgElement("line", "model-panel__dial-tick", {
          x1: start.x.toFixed(2),
          y1: start.y.toFixed(2),
          x2: end.x.toFixed(2),
          y2: end.y.toFixed(2),
          stroke: "currentColor",
          "stroke-opacity": "0.7",
          "stroke-width": "1.5"
        }));
      });

      const tip = phasePoint(dial.cx, cy, 34, dial.phase);
      group.append(makeSvgElement("line", `model-panel__dial-hand ${dial.handClass}`, {
        x1: dial.cx,
        y1: cy,
        x2: tip.x.toFixed(2),
        y2: tip.y.toFixed(2),
        stroke: "currentColor",
        "stroke-width": "3.5",
        "stroke-linecap": "round"
      }));
      group.append(makeSvgElement("circle", "model-panel__dial-tip", {
        cx: tip.x.toFixed(2),
        cy: tip.y.toFixed(2),
        r: "3.5",
        fill: "currentColor"
      }));
      group.append(makeSvgElement("circle", "model-panel__dial-hub", {
        cx: dial.cx,
        cy,
        r: "3",
        fill: "currentColor"
      }));
      group.append(makeSvgElement("text", "model-panel__dial-label", {
        x: dial.cx,
        y: "137",
        fill: "currentColor",
        "font-family": "system-ui, sans-serif",
        "font-size": "14",
        "font-weight": "700",
        "text-anchor": "middle"
      }, dial.label));
      group.append(makeSvgElement("text", "model-panel__dial-value", {
        x: dial.cx,
        y: "160",
        fill: "currentColor",
        "font-family": "ui-monospace, monospace",
        "font-size": "12",
        "text-anchor": "middle"
      }, dial.value));
      svg.append(group);
    });

    figure.append(caption, svg);
    return figure;
  }

  window.mountModelPanel = function mountModelPanel(host, state) {
    const tail = state && typeof state.tail === "string" ? state.tail : null;
    const hasMappedTail = Object.prototype.hasOwnProperty.call(Q_BY_TAIL, tail);
    const q = hasMappedTail ? Q_BY_TAIL[tail] : 0;
    const routeLabel = hasMappedTail
      ? `Selected tail: ${tail}`
      : tail === null
        ? "No route selected"
        : "Unmapped route (shown with the no-route value)";

    // q is an integer, so the ideal first phase is exactly zero modulo 2 pi.
    // The second phase is evaluated with finite-precision browser numbers.
    const theta1 = 0;
    const theta2 = wrap(TAU * q * Math.SQRT2);
    const distance1 = distanceToZero(theta1);
    const distance2 = distanceToZero(theta2);
    const insideReferenceGate = distance1 < REFERENCE_DELTA && distance2 < REFERENCE_DELTA;

    const panel = makeElement("section", "journey-panel model-panel");
    panel.setAttribute("aria-labelledby", "model-panel-title");

    const kicker = makeElement("p", "model-panel__eyebrow", "Signal 2 · idealized phase model");
    const title = makeElement("h2", "model-panel__title", "Two phases, one chosen coordinate");
    title.id = "model-panel-title";
    const intro = makeElement(
      "p",
      "model-panel__intro",
      "This route-to-q map is an arbitrary choice for the reading experiment. The language tail does not cause or predict an oscillator state."
    );

    const mapHeading = makeElement("h3", "model-panel__subheading", "Creator-chosen route map");
    const routeMap = makeElement("ul", "model-panel__route-map");
    ["ra → q = 2", "le → q = 5", "hu → q = 7", "no route → q = 0"].forEach((mapping) => {
      routeMap.append(makeElement("li", "", mapping));
    });

    const selected = makeElement("p", "model-panel__selected", routeLabel);
    const qLine = makeElement("p", "model-panel__q");
    qLine.append(document.createTextNode("Chosen q = "));
    qLine.append(makeElement("strong", "", String(q)));

    const formulaHeading = makeElement("h3", "model-panel__subheading", "Ideal-model formulas");
    const formulas = makeElement("div", "model-panel__formulas");
    formulas.append(makeElement("p", "", "theta1 = (2 pi q) mod 2 pi"));
    formulas.append(makeElement("p", "", "theta2 = (2 pi q sqrt(2)) mod 2 pi"));
    const phaseDialFigure = makePhaseDialFigure(q, theta1, theta2);

    const summaryHeading = makeElement("h3", "model-panel__subheading", "Computed phase summary");
    const summary = makeElement("dl", "model-panel__summary");
    const summaryRows = [
      ["theta1", formatRadians(theta1)],
      ["theta2", formatRadians(theta2)],
      ["shortest distance 1 → zero", formatRadians(distance1)],
      ["shortest distance 2 → zero", formatRadians(distance2)]
    ];
    summaryRows.forEach(([label, value]) => {
      const row = makeElement("div", "model-panel__summary-row");
      row.append(makeElement("dt", "", label));
      row.append(makeElement("dd", "", value));
      summary.append(row);
    });

    const gateStatus = makeElement(
      "p",
      `model-panel__gate${insideReferenceGate ? " is-inside" : " is-outside"}`,
      `${insideReferenceGate ? "Inside" : "Outside"} the illustrative delta = 0.50 rad gate`
    );
    const gateNote = makeElement(
      "p",
      "model-panel__note",
      "The gate uses the source note's strict rule: both shortest circular distances must be below 0.50 rad. It is a toy display rule."
    );
    const precisionNote = makeElement(
      "p",
      "model-panel__caveat",
      "COMPUTER ARITHMETIC · Math.PI and Math.SQRT2 are finite-precision JavaScript Number values; the phase summary is rounded to three decimals. This is not a measurement, physical observation, or scientific result, and it cannot establish that any physical rate ratio is irrational."
    );
    precisionNote.id = "model-panel-caveat";
    panel.setAttribute("aria-describedby", "model-panel-caveat");

    panel.append(
      kicker,
      title,
      intro,
      mapHeading,
      routeMap,
      selected,
      qLine,
      formulaHeading,
      formulas,
      phaseDialFigure,
      summaryHeading,
      summary,
      gateStatus,
      gateNote,
      precisionNote
    );
    host.replaceChildren(panel);
  };
})();
