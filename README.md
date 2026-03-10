<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Mini Minecraft 2D - Criativo</title>
  <style>
    body {
      margin: 0;
      background: #0a0a0a;
      color: #fff;
      font-family: Arial, Helvetica, sans-serif;
      text-align: center;
      overflow: hidden;
    }

    h1 {
      margin: 15px 0 5px;
      text-shadow: 0 0 15px #00ff00;
      font-size: 2.8rem;
    }

    #instructions {
      margin: 8px 0 15px;
      font-size: 1.1rem;
      color: #aaa;
    }

    canvas {
      border: 8px solid #444;
      border-radius: 12px;
      box-shadow: 0 0 30px rgba(0, 255, 0, 0.3);
      image-rendering: pixelated;
      background: #87CEEB;
    }

    #hotbar {
      display: flex;
      gap: 12px;
      justify-content: center;
      margin: 20px auto;
      padding: 10px;
      background: rgba(0, 0, 0, 0.7);
      border-radius: 12px;
      width: fit-content;
      border: 4px solid #555;
    }

    .slot {
      width: 68px;
      height: 68px;
      background-size: cover;
      border: 5px solid #666;
      border-radius: 10px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      font-size: 42px;
      cursor: pointer;
      transition: all 0.2s;
      box-shadow: 0 5px 15px rgba(0,0,0,0.6);
      position: relative;
    }

    .slot small {
      position: absolute;
      bottom: 4px;
      font-size: 14px;
      color: white;
      text-shadow: 0 0 5px black;
    }

    .slot.selected {
      border-color: #ffeb3b;
      box-shadow: 0 0 20px #ffeb3b;
      transform: scale(1.12);
    }

    button {
      margin-top: 10px;
      padding: 12px 28px;
      font-size: 1.2rem;
      background: #e74c3c;
      color: white;
      border: none;
      border-radius: 8px;
      cursor: pointer;
    }

    button:hover {
      background: #c0392b;
    }
  </style>
</head>
<body>

  <h1>🌍 Mini Minecraft 2D</h1>
  <p id="instructions">
    WASD ou ↑↓←→ = Voar • Clique esquerdo = Minerar • Clique direito = Colocar<br>
    Teclas 1️⃣ a 5️⃣ = Trocar bloco • R = Novo mundo
  </p>

  <canvas id="game" width="800" height="480"></canvas>

  <div id="hotbar"></div>

  <button id="newWorld">🌱 Novo Mundo</button>

  <script>
    const canvas = document.getElementById('game');
    const ctx = canvas.getContext('2d');
    const TILE = 32;
    const COLS = 25;
    const ROWS = 15;

    let world = [];
    let selectedBlock = 1;
    let playerX = 400;
    let playerY = 150;
    let keys = {};
    let mouseX = 0;
    let mouseY = 0;

    const blockData = [
      { id: 1, emoji: '🌿', color: '#4a8c2f', name: 'Grama' },
      { id: 2, emoji: '🟫', color: '#8b5a2b', name: 'Terra' },
      { id: 3, emoji: '🪨', color: '#555555', name: 'Pedra' },
      { id: 4, emoji: '🪵', color: '#a0522d', name: 'Madeira' },
      { id: 5, emoji: '🍃', color: '#2e8b57', name: 'Folhas' }
    ];

    const blockColors = {};
    blockData.forEach(b => blockColors[b.id] = b.color);

    const hotbar = document.getElementById('hotbar');

    function createHotbar() {
      hotbar.innerHTML = '';
      blockData.forEach((block) => {
        const slot = document.createElement('div');
        slot.className = 'slot';
        slot.style.backgroundColor = block.color;
        slot.innerHTML = `${block.emoji}<br><small>${block.id}</small>`;
        slot.dataset.id = block.id;
        slot.onclick = () => {
          selectedBlock = block.id;
          updateHotbar();
        };
        hotbar.appendChild(slot);
      });
      updateHotbar();
    }

    function updateHotbar() {
      document.querySelectorAll('.slot').forEach(slot => {
        slot.classList.toggle('selected', parseInt(slot.dataset.id) === selectedBlock);
      });
    }

    function generateWorld() {
      world = Array.from({ length: ROWS }, () => Array(COLS).fill(0));

      const baseY = Math.floor(ROWS * 0.65);

      for (let x = 0; x < COLS; x++) {
        const height = baseY + Math.floor(Math.random() * 3) - 1;
        for (let y = height; y < ROWS; y++) {
          if (y === height) world[y][x] = 1;           // grama
          else if (y < height + 4) world[y][x] = 2;    // terra
          else world[y][x] = 3;                        // pedra
        }
      }

      // Árvores aleatórias
      for (let i = 0; i < 7; i++) {
        const tx = 3 + Math.floor(Math.random() * (COLS - 6));
        for (let y = 0; y < ROWS; y++) {
          if (world[y][tx] === 1) {
            // Tronco
            if (y - 1 >= 0) world[y - 1][tx] = 4;
            if (y - 2 >= 0) world[y - 2][tx] = 4;
            if (y - 3 >= 0) world[y - 3][tx] = 4;
            // Folhas
            if (y - 4 >= 0) {
              world[y - 4][tx] = 5;
              if (tx - 1 >= 0) world[y - 4][tx - 1] = 5;
              if (tx + 1 < COLS) world[y - 4][tx + 1] = 5;
            }
            if (y - 5 >= 0) world[y - 5][tx] = 5;
            break;
          }
        }
      }
    }

    function draw() {
      // Céu
      ctx.fillStyle = '#87CEEB';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Nuvens simples
      ctx.fillStyle = 'rgba(255,255,255,0.7)';
      ctx.fillRect(80, 60, 180, 35);
      ctx.fillRect(220, 45, 140, 35);
      ctx.fillRect(520, 80, 160, 30);

      // Blocos
      for (let y = 0; y < ROWS; y++) {
        for (let x = 0; x < COLS; x++) {
          const type = world[y][x];
          if (type === 0) continue;
          ctx.fillStyle = blockColors[type];
          ctx.fillRect(x * TILE, y * TILE, TILE, TILE);
          
          // Bordas leves
          ctx.strokeStyle = 'rgba(0,0,0,0.4)';
          ctx.lineWidth = 2;
          ctx.strokeRect(x * TILE, y * TILE, TILE, TILE);
        }
      }

      // Jogador (Steve simplificado)
      // Cabeça
      ctx.fillStyle = '#f5c8a8';
      ctx.fillRect(playerX + 8, playerY, 18, 18);
      // Olhos
      ctx.fillStyle = '#000';
      ctx.fillRect(playerX + 12, playerY + 6, 4, 4);
      ctx.fillRect(playerX + 20, playerY + 6, 4, 4);
      // Corpo
      ctx.fillStyle = '#2e7dff';
      ctx.fillRect(playerX + 6, playerY + 18, 22, 22);
      // Pernas
      ctx.fillStyle = '#222';
      ctx.fillRect(playerX + 8, playerY + 38, 8, 12);
      ctx.fillRect(playerX + 18, playerY + 38, 8, 12);
    }

    function gameLoop() {
      const speed = 5;

      if (keys['a'] || keys['arrowleft']) playerX -= speed;
      if (keys['d'] || keys['arrowright']) playerX += speed;
      if (keys['w'] || keys['arrowup']) playerY -= speed;
      if (keys['s'] || keys['arrowdown']) playerY += speed;

      // Limites da tela
      playerX = Math.max(0, Math.min(canvas.width - 32, playerX));
      playerY = Math.max(0, Math.min(canvas.height - 50, playerY));

      draw();
      requestAnimationFrame(gameLoop);
    }

    function getTileFromMouse() {
      const tx = Math.floor(mouseX / TILE);
      const ty = Math.floor(mouseY / TILE);
      return { tx, ty };
    }

    // Mouse
    canvas.addEventListener('mousemove', (e) => {
      const rect = canvas.getBoundingClientRect();
      mouseX = e.clientX - rect.left;
      mouseY = e.clientY - rect.top;
    });

    canvas.addEventListener('click', (e) => {
      if (e.button === 0) { // esquerdo = minerar
        const { tx, ty } = getTileFromMouse();
        if (tx >= 0 && tx < COLS && ty >= 0 && ty < ROWS) {
          world[ty][tx] = 0;
        }
      }
    });

    canvas.addEventListener('contextmenu', (e) => {
      e.preventDefault();
      const { tx, ty } = getTileFromMouse();
      if (tx >= 0 && tx < COLS && ty >= 0 && ty < ROWS && world[ty][tx] === 0) {
        world[ty][tx] = selectedBlock;
      }
    });

    // Teclado
    window.addEventListener('keydown', (e) => {
      keys[e.key.toLowerCase()] = true;

      if (e.key >= '1' && e.key <= '5') {
        selectedBlock = parseInt(e.key);
        updateHotbar();
      }

      if (e.key.toLowerCase() === 'r') {
        generateWorld();
      }
    });

    window.addEventListener('keyup', (e) => {
      keys[e.key.toLowerCase()] = false;
    });

    // Botão Novo Mundo
    document.getElementById('newWorld').addEventListener('click', () => {
      generateWorld();
    });

    // Iniciar jogo
    function startGame() {
      createHotbar();
      generateWorld();
      draw();
      gameLoop();
    }

    startGame();
  </script>

</body>
</html>{
