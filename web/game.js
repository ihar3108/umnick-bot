const lvlDiv   = document.getElementById('lvl');
const qDiv     = document.getElementById('q');
const ansDiv   = document.getElementById('answers');
const b50      = document.getElementById('b50');
const aud      = document.getElementById('aud');

let lvl   = 1;
let qData = {};   // прилетит из бота

Telegram.WebApp.ready();
Telegram.WebApp.expand();

function renderQuestion(data) {
  qDiv.textContent = data.q;
  ansDiv.innerHTML = '';
  data.answers.forEach((a, i) => {
    const btn = document.createElement('button');
    btn.textContent = a;
    btn.onclick = () => answer(i);
    ansDiv.appendChild(btn);
  });
  lvlDiv.textContent = `Уровень ${lvl}`;
}

function answer(idx) {
  Telegram.WebApp.sendData(JSON.stringify({action:'answer', lvl, idx}));
}

b50.onclick = () => {
  Telegram.WebApp.sendData(JSON.stringify({action:'50', lvl}));
};
aud.onclick = () => {
  Telegram.WebApp.sendData(JSON.stringify({action:'aud', lvl}));
};

// первый вопрос прилетает из бота
window.addEventListener('message', e => {
  if (e.data.type === 'question') renderQuestion(e.data.payload);
});