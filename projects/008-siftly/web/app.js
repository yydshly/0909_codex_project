const expand = document.getElementById('expand');
const dialog = document.getElementById('poster-dialog');
const closePoster = document.getElementById('close-poster');
if (typeof dialog.showModal === 'function') {
  expand.hidden = false;
  expand.addEventListener('click', () => {
    dialog.showModal();
    document.body.classList.add('modal-open');
    closePoster.focus();
  });
  closePoster.addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => {
    document.body.classList.remove('modal-open');
    expand.focus();
  });
}
