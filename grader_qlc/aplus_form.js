const qlcaug = (data) => {

  const log = [];

  const logAdd = (entry) => {
    entry.time = new Date().getTime();
    log.push(entry);
  };

  const postUrl = (post_url_src) => {
    const path = document.location.pathname.split('/').slice(1);
    let url = post_url_src;
    for (let i = 0; i < path.length; i++) {
      url = url.replace(`%${i}`, path[i]);
    }
    return url;
  };

  logAdd({ type: 'init', files: data.files, qlcs: data.qlcs });
  console.log(data);

  let form = document.getElementById('qlc-form');

  form.appendChild(SimpleQuizForm(
    data.qlcs,
    (qIndex, optionIndex, isChecked, correct, max) => {
      console.log(`state ${correct}/${max}`);
    }
  ));

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const data = new FormData();
    data.append(data.post_field, JSON.stringify(log));
    fetch(postUrl(data.post_url), {method: 'POST', body: data});
  });
};
