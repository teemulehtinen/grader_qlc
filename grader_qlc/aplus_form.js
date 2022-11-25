const qlcaug = (data) => {

  const log = [];
  let logDirty = false;
  let allTouched = false;
  let allSolved = false;

  const logAdd = (entry) => {
    entry.time = new Date().getTime();
    log.push(entry);
    logDirty = true;
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

  logAdd({ type: 'init', files: data.files, qlcs: data.qlcs });

  // TODO display each file

  let form = document.getElementById('qlc-form');
  form.appendChild(SimpleQuizForm(
    data.qlcs,
    (qIndex, optionIndex, isChecked, solved, touched, total) => {
      const qlc = data.qlcs[qIndex];
      const opt = qlc.options[optionIndex];
      logAdd({ qlc: qlc.type, opt: opt.type, val: opt.answer, checked: isChecked });
      if (!allTouched && touched >= total) {
        logSend();
        allTouched = true;
      } else if (!allSolved && solved >= total) {
        logSend();
        allSolved = true;
      }
    }
  ));

  addEventListener('beforeunload', (event) => logSend());
};
