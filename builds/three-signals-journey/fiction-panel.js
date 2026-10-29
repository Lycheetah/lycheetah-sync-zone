(function () {
  'use strict';

  // The state argument is part of the panel contract and is intentionally ignored.
  // Route choices do not select story text or reveal anything about the reader.
  window.mountFictionPanel = function mountFictionPanel(host, state) {
    void state;
    if (!host || typeof host.appendChild !== 'function') return;

    var panel = document.createElement('section');
    panel.className = 'fiction-panel';
    panel.setAttribute('aria-label', 'Optional fictional scene');

    function clearPanel() {
      if (panel.parentNode) panel.parentNode.removeChild(panel);
    }

    function makeButton(label, action) {
      var button = document.createElement('button');
      button.type = 'button';
      button.textContent = label;
      button.addEventListener('click', action);
      return button;
    }

    function appendIntro() {
      var heading = document.createElement('h2');
      heading.textContent = 'Optional fictional scene';
      panel.appendChild(heading);

      var note = document.createElement('p');
      note.textContent = 'Fiction from the Unspent Hour, not a real practice or treatment. Your route selection is not used to infer feelings, beliefs, or needs. No response is requested or saved.';
      panel.appendChild(note);

      var openButton = makeButton('Open vignette', showVignette);
      panel.appendChild(openButton);
      panel.appendChild(makeButton('Skip scene', clearPanel));
      panel.appendChild(makeButton('Close panel', clearPanel));
    }

    function showVignette() {
      panel.textContent = '';

      var heading = document.createElement('h2');
      heading.textContent = 'The map with room left';
      panel.appendChild(heading);

      var first = document.createElement('p');
      first.textContent = 'Between two clocks that never agreed, a quiet hour crossed a wide valley. No clock owned it, and no one kept it for later.';
      panel.appendChild(first);

      var second = document.createElement('p');
      second.textContent = 'A cartographer closed a star map while one corner was still blank. Later, a new curve caught their eye, and they opened another page. The blank remained without becoming a debt.';
      panel.appendChild(second);

      var note = document.createElement('p');
      note.textContent = 'This is only a made-up scene, not advice or an exercise. Nothing is required of you as you read.';
      panel.appendChild(note);

      panel.appendChild(makeButton('Close scene', clearPanel));
      panel.appendChild(makeButton('Skip scene', clearPanel));
    }

    appendIntro();
    host.appendChild(panel);
  };
}());
