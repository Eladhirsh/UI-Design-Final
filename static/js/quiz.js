// static/js/quiz.js
document.addEventListener('DOMContentLoaded', () => {
  const prevBtn      = document.getElementById('prevBtn');
  const nextBtn      = document.getElementById('nextBtn');
  const progressText = document.getElementById('progress');
  const questions    = Array.from(document.querySelectorAll('.question-step'));
  const total        = questions.length;
  let current        = 1;

  // holds drag answers: { q8: 'Chopped Cheese', ... }
  const dragAnswers = {};

  // show only question n
  function showQuestion(n) {
    questions.forEach(q => q.classList.add('d-none'));
    const qDiv = document.getElementById('q' + n);
    qDiv.classList.remove('d-none');
    progressText.textContent = `Question ${n} of ${total}`;
    prevBtn.disabled = (n === 1);
    nextBtn.textContent = (n === total ? 'Submit Quiz' : '→');

    // if this is a drag question and we've saved an answer, drop it now
    if (['q8','q9','q10'].includes('q'+n)) {
      restoreDropFor('q'+n);
    }
  }

  // submit or navigate
  prevBtn.addEventListener('click', () => {
    if (current > 1) showQuestion(--current);
  });
  nextBtn.addEventListener('click', () => {
    if (current < total) {
      showQuestion(++current);
    } else {
      saveState().then(() => window.location.href = '/submit_quiz');
    }
  });

  // collect & save everything
  function saveState() {
    const answers = {};
    for (let i = 1; i <= 7; i++) {
      const sel = document.querySelector(`input[name="q${i}"]:checked`);
      answers['q'+i] = sel ? sel.value : '';
    }
    ['q8','q9','q10'].forEach(q => {
      answers[q] = dragAnswers[q] || '';
    });
    return fetch('/save_state', {
      method: 'POST',
      headers: { 'Content-Type':'application/json' },
      body: JSON.stringify({ answers, last_question: current })
    });
  }
  document.querySelectorAll('input[type=radio]')
    .forEach(radio => radio.addEventListener('change', saveState));

  // center a dropped image in its map
  function dropImageToMap(qDiv, img) {
    const zone = qDiv.querySelector(`.dropzone[data-qid="${qDiv.id}"]`);
    const mapC = qDiv.querySelector('.map-container');
    const opts = qDiv.querySelector('.d-flex.flex-wrap');

    // send any previous one back
    mapC.querySelectorAll('.dish-img').forEach(e => {
      if (e !== img) {
        opts.appendChild(e);
        e.style.position = e.style.left = e.style.top = '';
      }
    });

    // place this one
    mapC.appendChild(img);
    img.style.position = 'absolute';
    const zr = zone.getBoundingClientRect(), cr = mapC.getBoundingClientRect();
    const cx = zr.left + zr.width/2  - cr.left;
    const cy = zr.top  + zr.height/2 - cr.top;
    img.style.left = `${cx - img.offsetWidth/2}px`;
    img.style.top  = `${cy - img.offsetHeight/2}px`;
  }

  // only drop once the map is visible & loaded
  function restoreDropFor(qid) {
    const val = dragAnswers[qid];
    if (!val) return;

    const qDiv = document.getElementById(qid);
    const img  = qDiv.querySelector(`.dish-img[data-name="${val}"]`);
    const mapImg = qDiv.querySelector('.map-container img.img-fluid');
    if (!img || !mapImg) return;

    const doDrop = () => dropImageToMap(qDiv, img);
    if (mapImg.complete) {
      doDrop();
    } else {
      mapImg.addEventListener('load', doDrop);
    }
  }

  // initial load: restore state, then showQuestion
  fetch('/get_state')
    .then(r => r.json())
    .then(state => {
      current = state.last_question || 1;
      // restore radios
      Object.entries(state.answers||{}).forEach(([qid,val]) => {
        const inp = document.querySelector(`input[name="${qid}"][value="${val}"]`);
        if (inp) inp.checked = true;
        if (['q8','q9','q10'].includes(qid) && val) {
          dragAnswers[qid] = val;
        }
      });
      showQuestion(current);
    });

  // drag & drop wiring
  document.querySelectorAll('.dish-img').forEach(img => {
    img.addEventListener('dragstart', e => {
      e.dataTransfer.setData('text/plain', img.id);

      // hide the browser’s drag-ghost
      const ghost = new Image();
      ghost.src = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==';
      e.dataTransfer.setDragImage(ghost, 0, 0);
    });
  });
  document.querySelectorAll('.dropzone').forEach(zone => {
    zone.addEventListener('dragover',  e => e.preventDefault());
    zone.addEventListener('dragenter',() => zone.classList.add('highlight'));
    zone.addEventListener('dragleave',() => zone.classList.remove('highlight'));
    zone.addEventListener('drop', e => {
      e.preventDefault();
      zone.classList.remove('highlight');
      const draggedId = e.dataTransfer.getData('text/plain');
      const dragged  = document.getElementById(draggedId);
      if (!dragged) return;
      const qDiv = zone.closest('.question-step');
      dropImageToMap(qDiv, dragged);

      // record & save
      dragAnswers[qDiv.id] = dragged.getAttribute('data-name');
      saveState();
    });
  });
});
