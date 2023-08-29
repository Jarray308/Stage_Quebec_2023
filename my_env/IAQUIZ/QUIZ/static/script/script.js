const showButton = document.getElementById('showButton');
const hideButton = document.getElementById('hideButton');
const textInputArea = document.getElementById('textInputArea');

showButton.addEventListener('click', () => {
  textInputArea.classList.remove('hidden');
});

hideButton.addEventListener('click', () => {
  textInputArea.classList.add('hidden');
});



