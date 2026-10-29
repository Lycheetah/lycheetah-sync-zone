(function () {
  "use strict";

  const groups = [
    {
      id: "science-number-code-science",
      title: "Science",
      items: [
        {
          label: "DERIVED · FINITE TOY",
          title: "Eight Stations, One Hop",
          description: "An exact gcd derivation for two fixed hops on Z/8Z, explicitly limited to a finite combinatorial rule.",
          links: [
            { href: "../../science/14_vire_eight-station-ring.md", text: "Read the ring note" }
          ]
        },
        {
          label: "INVENTED MODEL · CONDITIONAL MATH",
          title: "Two hands that never share a tick",
          description: "An ideal incommensurate phase model, followed by a q = 2 check that limits the claim about near returns.",
          links: [
            { href: "../../science/07_vire_quasi-clock-moire.md", text: "Read the model note" },
            { href: "../../science/09_vire_derived-counterexample.md", text: "Read the q = 2 check" }
          ]
        },
        {
          label: "INTERACTIVE BUILD",
          title: "Quasi-Clock Atlas",
          description: "An offline phase-map explorer for the ideal toy equations; its display is not a physical measurement.",
          links: [
            { href: "../quasi-clock-atlas/index.html", text: "Open the phase explorer" }
          ]
        }
      ]
    },
    {
      id: "science-number-code-numeracy",
      title: "Numeracy",
      items: [
        {
          label: "INVENTED NUMERACY",
          title: "p-Adic Ultrametric Analysis",
          description: "A speculative mapping from p-adic distance to hierarchical concept trees; the analogy is a proposal, not an observed cognitive law.",
          links: [
            { href: "../../numeracy/02_p-adic-ultrametric-analysis-and-fractal-concept-trees.md", text: "Read the p-adic note" }
          ]
        },
        {
          label: "INVENTED NUMERACY",
          title: "Adelic Analysis and Global-Local Harmony",
          description: "A speculative global/local number-system analogy. The atlas does not validate the source's mathematical or cognitive claims.",
          links: [
            { href: "../../numeracy/04_adelic-analysis-and-global-local-epistemic-harmony.md", text: "Read the adelic note" }
          ]
        },
        {
          label: "INTERACTIVE BUILD · SOURCE HAS ITS OWN LIMITS",
          title: "Sheaf-Valued Cellular Automaton",
          description: "A browser simulation on a hexagonal cell complex; the atlas links to it but does not run or independently verify it.",
          links: [
            { href: "../kineton-sheaf-automata/index.html", text: "Open the automaton" }
          ]
        }
      ]
    },
    {
      id: "science-number-code-code",
      title: "Code",
      items: [
        {
          label: "INVENTED SOURCE CODE",
          title: "Mathesis Philologica Engine",
          description: "Python source proposing several cross-domain components. This atlas links to the file; it does not execute or certify it.",
          links: [
            { href: "../../code/01_mathesis_philologica_engine.py", text: "Inspect the Python source" }
          ]
        },
        {
          label: "INVENTED SOURCE CODE",
          title: "Topological Morphogenesis Engine",
          description: "Python source for a discrete reaction-diffusion simulation; the link is for inspection, not a run result.",
          links: [
            { href: "../../code/06_topological_morphogenesis_engine.py", text: "Inspect the simulation source" }
          ]
        },
        {
          label: "INTERACTIVE READING BUILD",
          title: "Three Signals Journey",
          description: "An offline reading experiment joining an invented language route, an ideal phase toy, and optional fiction; its route map is arbitrary.",
          links: [
            { href: "../three-signals-journey/index.html", text: "Open the reading journey" }
          ]
        }
      ]
    }
  ];

  function makeCard(doc, item) {
    const card = doc.createElement("article");
    card.className = "atlas-card";

    const label = doc.createElement("span");
    label.className = "label";
    label.textContent = item.label;

    const heading = doc.createElement("h4");
    heading.textContent = item.title;

    const description = doc.createElement("p");
    description.textContent = item.description;

    card.append(label, heading, description);
    item.links.forEach(function (target) {
      const link = doc.createElement("a");
      link.href = target.href;
      link.textContent = target.text;
      card.append(link);
    });
    return card;
  }

  window.renderScienceNumberCode = function renderScienceNumberCode(host) {
    if (!host || typeof host.replaceChildren !== "function") return;

    const doc = host.ownerDocument || document;
    const section = doc.createElement("section");
    section.className = "atlas-science-number-code";
    section.setAttribute("aria-label", "Science, numeracy, and code reading paths");

    const introduction = doc.createElement("p");
    introduction.textContent = "Choose a source note or an optional browser build. These links are reading paths, not endorsements: this atlas does not independently verify claims or run code.";
    section.append(introduction);

    groups.forEach(function (group) {
      const category = doc.createElement("section");
      category.className = "atlas-group";
      category.setAttribute("aria-labelledby", group.id);

      const heading = doc.createElement("h3");
      heading.id = group.id;
      heading.textContent = group.title;
      category.append(heading);

      group.items.forEach(function (item) {
        category.append(makeCard(doc, item));
      });
      section.append(category);
    });

    host.replaceChildren(section);
  };
})();
