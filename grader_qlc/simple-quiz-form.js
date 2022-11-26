window.SimpleQuizForm = window.SimpleQuizForm || ((questions, callback) => {

  const styles = `
    .q-wrap .q-item {
      margin: 1em 0;
    }
    .q-wrap .q-item label {
      display: block;
      margin: 2px 0;
      border: 1px solid lightgrey;
      border-radius: 4px;
      cursor: pointer;
    }
    .q-wrap .q-item label:hover {
      background-color: gainsboro;
    }
    .q-wrap .q-item label.incorrect {
      background-color: salmon;
      color: darkred;
    }
    .q-wrap .q-item label.correct {
      background-color: springgreen;
      color: green;
    }
    .q-wrap .q-item label .info {
      margin-left: 2em;
    }
  `;

  const state = questions.map(q => ({
    correct: q.options.map(o => o.correct || false),
    selected: q.options.map(_ => false),
    solved: false,
    touched: false,
  }));

  const updateSolved = (qState) => {
    for (let i = 0; i < qState.correct.length; i += 1) {
      if (qState.selected[i] != qState.correct[i]) {
        qState.solved = false;
        return false;
      }
    }
    qState.solved = true;
    return true;
  };

  const selectOption = (qIndex, optionIndex, isChecked, many) => {
    const qState = state[qIndex];
    qState.touched = true;
    qState.selected = qState.selected.map(
      (old, i) => i === optionIndex ? isChecked : (many ? old : false)
    );
    return updateSolved(qState);
  };

  const reportState = (qIndex, optionIndex, isChecked, many) => {
    const isSolved = selectOption(qIndex, optionIndex, isChecked, many);
    setTimeout(() => callback(
      qIndex,
      optionIndex,
      isChecked,
      state.filter(qs => qs.solved).length,
      state.filter(qs => qs.touched).length,
      state.length
    ));
    return isSolved;
  };

  const addStyle = (css) => {
    const style = document.createElement('style');
    style.textContent = css;
    document.head.appendChild(style);
  };

  const mkElement = (tag, attrs, html, childNodes) => {
    const el = document.createElement(tag);
    if (attrs) {
      Object.entries(attrs).forEach(kv => el.setAttribute(kv[0], kv[1]));
    }
    if (html) {
      el.innerHTML = html;
    }
    if (childNodes) {
      childNodes.forEach(child => el.appendChild(child));
    }
    return el;
  };

  const displayInfo = (label, info) => {
    if (info && label.querySelector('span.info') === null) {
      label.appendChild(mkElement('span', { class: 'info' }, info));
    }
  };

  addStyle(styles);

  return mkElement(
    'div',
    { class: 'q-wrap' },
    '',
    questions.map((q, qIndex) => {
      const many = q.options.filter(o => o.correct).length > 1;
      return mkElement(
        'div',
        { class: 'q-item' },
        `<strong>${q.question}</strong>`,
        q.options.map((o, i) => {
          const label = mkElement(
            'label',
            {},
            `<input type="${many ? 'checkbox' : 'radio'}" name="q${qIndex}" value="${encodeURIComponent(o.answer)}"> ${o.answer}`
          );
          label.querySelector('input').addEventListener('change', evt => {
            const isChecked = evt.target.checked;
            if (!many) {
              label.parentNode.querySelectorAll('label').forEach(
                l => l.removeAttribute('class')
              );
            }
            if (isChecked) {
              label.setAttribute('class', o.correct ? 'correct' : 'incorrect');
            } else {
              label.removeAttribute('class');
            }
            if (reportState(qIndex, i, isChecked, many)) {
              label.parentNode.querySelectorAll('label').forEach(
                (l, i) => displayInfo(l, q.options[i].info)
              );
              label.parentNode.querySelectorAll('input').forEach(
                (e) => { e.disabled = true; }
              );
            } else {
              displayInfo(label, o.info);
            }
          });
          return label;
        })
      );
    })
  );
});