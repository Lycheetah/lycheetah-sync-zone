(function () {
  'use strict';

  const allowedTails = new Set(['ra', 'le', 'hu']);
  let panelSequence = 0;

  const choices = [
    {
      key: 'none',
      value: null,
      label: 'No route',
      detail: 'Leave this sample without a route tail.'
    },
    {
      key: 'ra',
      value: 'ra',
      label: '=ra · return',
      detail: 'Echo the handle back to the speaker for another pass.'
    },
    {
      key: 'le',
      value: 'le',
      label: '=le · lend',
      detail: 'Leave the handle available for anyone who chooses to carry it.'
    },
    {
      key: 'hu',
      value: 'hu',
      label: '=hu · harbor',
      detail: 'Keep the handle open without requiring an immediate reply.'
    }
  ];

  window.mountLanguagePanel = function mountLanguagePanel(host, state, update) {
    if (!host || typeof host.replaceChildren !== 'function' || typeof update !== 'function') return;

    const doc = host.ownerDocument || document;
    const panelId = 'rillwire-route-' + (++panelSequence);
    const incomingTail = state ? state.tail : null;
    const currentTail = incomingTail === null || incomingTail === undefined
      ? null
      : allowedTails.has(incomingTail)
        ? incomingTail
        : undefined;

    const panel = doc.createElement('section');
    panel.className = 'journey-language-panel';

    const title = doc.createElement('h2');
    title.textContent = 'Choose a Rillwire route';

    const introduction = doc.createElement('p');
    introduction.id = panelId + '-introduction';
    introduction.textContent = 'This journey offers three invented sentence-final tails, or no route. The choice only describes how a topic may travel in this sample.';

    const boundary = doc.createElement('p');
    boundary.id = panelId + '-boundary';
    boundary.textContent = 'It does not say whether a claim is true or whether anyone consents. Nothing is sent or saved.';

    const fieldset = doc.createElement('fieldset');
    fieldset.className = 'journey-route-options';
    fieldset.setAttribute('aria-describedby', introduction.id + ' ' + boundary.id);

    const legend = doc.createElement('legend');
    legend.textContent = 'Route tail';
    fieldset.appendChild(legend);

    const name = panelId + '-choice';
    choices.forEach(function (choice) {
      const row = doc.createElement('div');
      row.className = 'journey-route-option';

      const input = doc.createElement('input');
      input.type = 'radio';
      input.name = name;
      input.id = panelId + '-' + choice.key;
      input.value = choice.value === null ? '' : choice.value;
      input.checked = currentTail !== undefined && choice.value === currentTail;

      const label = doc.createElement('label');
      label.htmlFor = input.id;
      label.className = 'journey-route-label';

      const nameText = doc.createElement('span');
      nameText.className = 'journey-route-name';
      nameText.textContent = choice.label;

      const detailText = doc.createElement('span');
      detailText.className = 'journey-route-detail';
      detailText.textContent = choice.detail;

      label.append(nameText, detailText);
      row.append(input, label);
      fieldset.appendChild(row);

      input.addEventListener('change', function () {
        if (!input.checked) return;
        update({ tail: choice.value });
      });
    });

    const note = doc.createElement('p');
    note.className = 'journey-route-note';
    note.textContent = 'These are local, fictional routing labels, not commands. The larger Rillwire sketch includes other tails that this journey does not model.';

    panel.append(title, introduction, boundary, fieldset, note);
    host.replaceChildren(panel);
  };
})();
