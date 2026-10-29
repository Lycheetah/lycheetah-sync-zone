(function () {
  'use strict';

  const paths = [
    {
      href: '../../language/04_glossa_tide-grammar.md',
      title: 'Tide Grammar · invented',
      description: 'Opening particles sketch seen, reasoned, maybe, and story footing. Reader comprehension is untested.'
    },
    {
      href: '../../language/05_riv_register-of-echoes.md',
      title: 'Rillwire Echo Register · invented',
      description: 'Sentence-final tails offer ways for a topic-handle to circulate; they do not mark truth or permission.'
    },
    {
      href: '../../language/06_cadence_future-echo-script.md',
      title: 'Farloom Future-Echo Script · invented',
      description: 'A story-time frame places events before, during, or beyond an imagined horizon; it is not a forecast.'
    },
    {
      href: '../../language/07_riv_ambiguity-lab.md',
      title: 'Tide and Rillwire Ambiguity Lab · invented',
      description: 'Context prompts distinguish the sketches’ stated conventions from unresolved readings; no reader session was run.'
    },
    {
      href: '../../language/10_riv_two-channel-dialogue.md',
      title: 'Two Channels, One Conversation · invented',
      description: 'A short dialogue keeps Tide footing particles and Rillwire routing tails as separate mechanisms.'
    }
  ];

  window.renderLanguagePaths = function renderLanguagePaths(host) {
    if (!host || typeof host.replaceChildren !== 'function') return;

    const doc = host.ownerDocument || document;
    const section = doc.createElement('section');
    section.className = 'atlas-language-paths';
    section.setAttribute('aria-label', 'Invented language reading paths');

    const title = doc.createElement('h2');
    title.textContent = 'Language paths';

    const introduction = doc.createElement('p');
    introduction.textContent = 'A few invented forms to read side by side. These links point to source notes; the atlas does not validate their claims or test reader comprehension.';

    const list = doc.createElement('ul');
    list.className = 'atlas-language-list';

    paths.forEach(function (path) {
      const item = doc.createElement('li');
      const link = doc.createElement('a');
      link.href = path.href;
      link.textContent = path.title;

      const description = doc.createElement('p');
      description.textContent = path.description;

      item.append(link, description);
      list.appendChild(item);
    });

    section.append(title, introduction, list);
    host.replaceChildren(section);
  };
})();
