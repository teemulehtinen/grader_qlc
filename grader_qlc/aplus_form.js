window.QLCAugment = window.QLCAugment || ((data) => {

  const log = [];
  let logDirty = false;
  let allTouched = false;
  let allSolved = false;

  const logAdd = (entry, dirty) => {
    entry.time = new Date().getTime();
    log.push(entry);
    logDirty = dirty === undefined || dirty;
  };

  const postUrl = (post_url_src) => {
    const path = document.location.pathname.split('/').slice(1);
    let url = post_url_src;
    for (let i = 0; i < path.length; i++) {
      url = url.replace(`%${i}`, path[i]);
    }
    return url;
  };

  const logSend = () => {
    if (logDirty) {
      const body = new FormData();
      body.append(data.post_field, JSON.stringify(log));
      fetch(postUrl(data.post_url), {method: 'POST', body}).then(() => {
        logDirty = false;
      });
    }
  };

  logAdd({ type: 'init', files: data.files, qlcs: data.qlcs }, false);
  addEventListener('beforeunload', (event) => logSend());

  let form = document.getElementById('qlc-form');
  form.appendChild(SimpleQuizForm(
    data.qlcs,
    (qIndex, optionIndex, isChecked, solved, touched, total) => {
      const qlc = data.qlcs[qIndex];
      const opt = qlc.options[optionIndex];
      logAdd({
        qlc: qlc.type,
        opt: opt.type,
        answer: opt.answer,
        correct: opt.correct,
        checked: isChecked,
        solved,
      });
      if (!allTouched && touched >= total) {
        logSend();
        allTouched = true;
      } else if (!allSolved && solved >= total) {
        logSend();
        allSolved = true;
      }
    }
  ));

  let div = document.getElementById('qlc-files');
  data.files.forEach(entry => {
    let h4 = document.createElement('h4');
    h4.innerHTML = entry[0];
    div.appendChild(h4);
    let pre = document.createElement('pre');
    //pre.setAttribute('class', 'hljs');
    pre.innerHTML = entry[1];
    div.appendChild(pre);
    if ($ !== undefined) {
      $(pre).highlightCode();
    }
  });
  const style = document.head.lastElementChild;
  style.textContent = (
    style.textContent +
    '\n#qlc-files p { display: none; }'
    //+'\n#qlc-files table.src tr td.src { white-space: pre; }'
  );

  document.querySelector('#page-modal .modal-dialog').setAttribute('style', 'width:1200px;');
});