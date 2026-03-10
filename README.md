><!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Jogo da Memória - Simples</title>
  <style>
    body {
      margin: 0;
      height: 100vh;
      background: linear-gradient(135deg, #1e3c72, #2a5298);
      font-family: Arial, sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      color: white;
    }

    h1 {
      margin: 20px 0;
      text-shadow: 0 0 10px rgba(255,255,255,0.8);
    }

    #info {
      margin: 10px;
      font-size: 1.2rem;
    }

    #game-board {
      display: grid;
      grid-template-columns: repeat(4, 90px);
      grid-gap: 15px;
      perspective: 1000px;
    }

    .card {
      width: 90px;
      height: 120px;
      position: relative;
      transform-style: preserve-3d;
      transition: transform 0.6s;
      cursor: pointer;
    }

    .card.flipped {
      transform: rotateY(180deg);
    }

    .card-front, .card-back {
      position: absolute;
      width: 100%;
      height: 100%;
      backface-visibility: hidden;
      border-radius: 12px;
      box-shadow: 0 4px 8px rgba(0,0,0,0.4);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 3rem;
    }

    .card-front {
      background: #f39c12;
      color: white;
      transform: rotateY(180deg);
    }

    .card-back {
      background: linear-gradient(45deg, #3498db, #2980b9);
      color: #ecf0f1;
    }

    .card.matched .card-front {
      background: #27ae60;
    }

    button {
      margin-top: 20px;
      padding: 12px 30px;
      font-size: 1.2rem;
      background: #e74c3c;
      color: white;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      transition: background 0.3s;
    }

    button:hover {
      background: #c0392b;
    }
  </style>
</head>
<body>

  <h1>Jogo da Memória</h1>
  <div id="info">Movimentos: 0 | Tempo: 0s</div>

  <div id="game-board"></div>

  <button id="restart">Jogar Novamente</button>

  <script>
    const emojis = ['🍎','🍌','🍇','🍉','🍓','🍒','🍍','🥝'];
    let cards = [...emojis, ...emojis]; // 16 cartas (8 pares)
    let flippedCards = [];
    let matchedPairs = 0;
    let moves = 0;
    let timer = 0;
    let timerInterval;

    const board = document.getElementById('game-board');
    const info = document.getElementById('info');
    const restartBtn = document.getElementById('restart');

    function shuffle(array) {
      for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
      }
      return array;
    }

    function createCard(emoji) {
      const card = document.createElement('div');
      card.classList.add('card');

      const front = document.createElement('div');
      front.classList.add('card-front');
      front.textContent = emoji;

      const back = document.createElement('div');
      back.classList.add('card-back');
      back.textContent = '?';

      card.appendChild(front);
      card.appendChild(back);

      card.addEventListener('click', () => flipCard(card, emoji));

      return card;
    }

    function startGame() {
      board.innerHTML = '';
      cards = shuffle(cards);
      matchedPairs = 0;
      moves = 0;
      timer = 0;
      flippedCards = [];
      clearInterval(timerInterval);
      updateInfo();

      cards.forEach(emoji => {
        const cardElem = createCard(emoji);
        board.appendChild(cardElem);
      });

      timerInterval = setInterval(() => {
        timer++;
        updateInfo();
      }, 1000);
    }

    function flipCard(card, emoji) {
      if (flippedCards.length === 2 || card.classList.contains('flipped') || card.classList.contains('matched')) return;

      card.classList.add('flipped');
      flippedCards.push({card, emoji});

      if (flippedCards.length === 2) {
        moves++;
        updateInfo();

        setTimeout(checkMatch, 800);
      }
    }

    function checkMatch() {
      const [first, second] = flippedCards;

      if (first.emoji === second.emoji) {
        first.card.classList.add('matched');
        second.card.classList.add('matched');
        matchedPairs++;

        if (matchedPairs === emojis.length) {
          clearInterval(timerInterval);
          setTimeout(() => alert(`Parabéns! Você venceu!\nMovimentos: ${moves}\nTempo: ${timer}s`), 500);
        }
      } else {
        first.card.classList.remove('flipped');
        second.card.classList.remove('flipped');
      }

      flippedCards = [];
    }

    function updateInfo() {
      info.textContent = `Movimentos: ${moves} | Tempo: ${timer}s`;
    }

    restartBtn.addEventListener('click', startGame);

    // Inicia o jogo na primeira vez
    startGame();
  </script>

</body>
</html>