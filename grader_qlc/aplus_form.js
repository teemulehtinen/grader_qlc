console.log(document.location);

let form = document.getElementById('qlc-form');
form.addEventListener('submit', (event) => {
  event.preventDefault();
  const data = new FormData();
  data.append('log_json', '[0, 1]');
  fetch(form.getAttribute('action'), { method: 'POST', body: data});
});
