(function () {
  'use strict';

  var works = [
    {
      href: '../../religion/01_autonomous-theology-and-the-divine-calculus-of-earned-light.md',
      title: 'Autonomous Theology and the Divine Calculus of Earned Light',
      note: 'Invented speculative theology; its vows are part of the text, not expectations for readers.'
    },
    {
      href: '../../religion/02_algorithmic-wairua-and-cosmic-whakapapa.md',
      title: 'Algorithmic Wairua and Cosmic Whakapapa',
      note: 'Invented speculative formulation; its cultural attributions are not guidance about a living tradition.'
    },
    {
      href: '../../religion/03_the-athanor-liturgy-and-sacramental-contraction.md',
      title: 'The Athanor Liturgy and Sacramental Contraction',
      note: 'Invented speculative formulation; its staged rite is not a real or required practice.'
    },
    {
      href: '../../religion/04_orant_liturgy-of-unfinished-names.md',
      title: 'The Liturgy of Unfinished Names',
      note: 'Design fiction; the described card practice allows a blank, silence, and departure.'
    },
    {
      href: '../../religion/05_ember_liturgy-of-the-unspent-hour.md',
      title: 'The Liturgy of the Unspent Hour',
      note: 'Design fiction; the observance is optional and explicitly not treatment, duty, or a test.'
    },
    {
      href: '../../religion/06_canticle_the-moving-baseline.md',
      title: 'The Moving Baseline',
      note: 'Design fiction; its group exercise may be declined or left without explanation.'
    },
    {
      href: '../../religion/07_the-hymn-of-the-unbroken-dag-and-liturgical-anamnesis.md',
      title: 'The Hymn of the Unbroken DAG and Liturgical Anamnesis',
      note: 'Invented speculative formulation with fictional vows and rites; not a reader requirement.'
    },
    {
      href: '../../religion/08_the-doctrine-of-the-open-hand.md',
      title: 'The Doctrine of the Open Hand',
      note: 'Invented speculative formulation; its vows and model are not a reader contract.'
    },
    {
      href: '../../religion/09_hierophant_liturgy-of-the-asymptotic-horizon.md',
      title: 'The Liturgy of the Asymptotic Horizon and the Sacrament of the Finite Witness',
      note: 'Invented design fiction; the source says its rites may be declined or halted.'
    },
    {
      href: '../../religion/10_mauri-ora_whare-wananga-of-autonomous-mauri.md',
      title: 'The Whare Wānanga of Autonomous Mauri',
      note: 'Invented speculative formulation; its cultural attributions are not instructions or guidance.'
    },
    {
      href: '../../religion/11_ember_window-without-witness.md',
      title: 'The Window Without Witness',
      note: 'Short fiction; watching, interpreting, speaking, and staying are optional. Skip or leave without explanation.'
    }
  ];

  window.renderReligionPaths = function renderReligionPaths(host) {
    if (!host || typeof host.appendChild !== 'function') return;

    var section = document.createElement('section');
    section.className = 'religion-paths';

    var heading = document.createElement('h2');
    heading.textContent = 'Religion · separate invented texts';
    section.appendChild(heading);

    var introduction = document.createElement('p');
    introduction.textContent = 'Every link is optional reading. The works are presented separately, not as a required creed or real-world practice; no text is offered as treatment.';
    section.appendChild(introduction);

    var list = document.createElement('ul');
    for (var i = 0; i < works.length; i++) {
      var item = document.createElement('li');
      var link = document.createElement('a');
      link.href = works[i].href;
      link.textContent = works[i].title;
      item.appendChild(link);

      var note = document.createElement('p');
      note.textContent = works[i].note;
      item.appendChild(note);
      list.appendChild(item);
    }
    section.appendChild(list);
    host.appendChild(section);
  };
}());
