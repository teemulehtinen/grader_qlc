const qlcaug = (json_data) => {

  const log = [];

  const log_add = (entry) => {
    entry.time = new Date().getTime();
    log.push(entry);
  };

  const post_url = (post_url_src) => {
    const path = document.location.pathname.split('/').slice(1);
    let url = post_url_src;
    for (let i = 0; i < path.length; i++) {
      url = url.replace(`%${i}`, path[i]);
    }
    return url;
  };

  log_add({ type: 'init', files: json_data.files, qlc: json_data.qlcs });
  console.log(json_data);

  let form = document.getElementById('qlc-form');
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const data = new FormData();
    data.append(json_data.post_field, JSON.stringify(log));
    fetch(post_url(json.post_url), {method: 'POST', body: data});
  });

};
