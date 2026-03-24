<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
  <title>Brawl Stars Mini - Escolha o Brawler</title>
  <style>
    body { margin:0; background:#111; overflow:hidden; touch-action:none; font-family: Arial, sans-serif; }
    canvas { display:block; margin:0 auto; background:#2a5; }
    #menu {
      position: absolute; top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(0,0,0,0.85); display: flex; flex-direction: column;
      align-items: center; justify-content: center; color: white; z-index: 100;
    }
    .brawler {
      width: 180px; height: 180px; margin: 15px; border: 5px solid #fff;
      border-radius: 20px; display: flex; align-items: center; justify-content: center;
      font-size: 80px; cursor: pointer; transition: 0.2s;
    }
    .brawler:hover { transform: scale(1.1); border-color: #00ffff; }
    #joystick {
      position: absolute; bottom: 30px; left: 30px;
      width: 130px; height: 130px;
      background: rgba(255,255,255,0.25);
      border: 3px solid rgba(255,255,255,0.6);
      border-radius: 50%;
      display: none;
      box-shadow: 0 0 20px rgba(0,0,0,0.5);
    }
    #fire {
      position: absolute; bottom: 40px; right: 40px;
      width: 90px; height: 90px;
      background: rgba(255,50,50,0.5);
      border: 4px solid #ff0;
      border-radius: 50%;
      display: none;
      font-size: 40px;
      align-items: center; justify-content: center;
      color: white; text-shadow: 0 0 10px black;
    }
    #score { position: absolute; top: 15px; left: 20px; color: white; font-size: 28px; font-weight: bold; text-shadow: 2px 2px 4px black; }
    #superBar { position: absolute; top: 55px; left: 20px; width: 220px; height: 20px; background: rgba(0,0,0,0.6); border: 3px solid #00ffff; border-radius: 10px; overflow: hidden; }
    #superFill { width: 0%; height: 100%; background: linear-gradient(90deg, #00ffff, #0088ff); }
    #superText { position: absolute; top: 80px; left: 20px; color: #00ffff; font-size: 18px; font-weight: bold; text-shadow: 0 0 8px #00ffff; opacity: 0; transition: opacity 0.4s; }
  </style>
</head>
<body>

  <div id="menu">
    <h1>Escolha seu Brawler</h1>
    <div style="display:flex; gap:30px;">
      <div class="brawler" onclick="selectBrawler(0)" style="background:#00aaff;">🔫</div>
      <div class="brawler" onclick="selectBrawler(1)" style="background:#ffaa00;">🏹</div>
      <div class="brawler" onclick="selectBrawler(2)" style="background:#ff4444;">🐂</div>
    </div>
    <p style="margin-top:20px;">Shelly &nbsp;&nbsp;&nbsp; Colt &nbsp;&nbsp;&nbsp; Bull</p>
  </div>

  <div id="score">Score: 0</div>
  <div id="superBar"><div id="superFill"></div></div>
  <div id="superText">SUPER PRONTO!</div>

  <canvas id="game"></canvas>
  <div id="joystick"></div>
  <div id="fire">🔫</div>

  <script>
    const canvas = document.getElementById('game');
    const ctx = canvas.getContext('2d');
    canvas.width = 800;
    canvas.height = 600;

    let player, bullets = [], enemies = [], particles = [], score = 0, superCharge = 0, isSuperReady = false;
    let keys = {}, mouseX = 400, mouseY = 300, lastShot = 0;
    let joystickActive = false, joystickX = 0, joystickY = 0, joyCenterX = 0, joyCenterY = 0;

    const scoreDiv = document.getElementById('score');
    const superFill = document.getElementById('superFill');
    const superText = document.getElementById('superText');
    const menu = document.getElementById('menu');

    // Brawlers
    const brawlers = [
      { name: "Shelly", color: "#00aaff", speed: 4.8, damage: 32, health: 100, superDamage: 60 },
      { name: "Colt",   color: "#ffaa00", speed: 4.3, damage: 28, health: 85,  superDamage: 45 },
      { name: "Bull",   color: "#ff4444", speed: 5.2, damage: 35, health: 130, superDamage: 70 }
    ];

    let currentBrawler = 0;

    function selectBrawler(id) {
      currentBrawler = id;
      menu.style.display = 'none';
      startGame();
    }

    const walls = [
      {x: 200, y: 170, w: 400, h: 30},
      {x: 200, y: 400, w: 400, h: 30},
      {x: 170, y: 190, w: 30, h: 220},
      {x: 600, y: 190, w: 30, h: 220}
    ];

    const bushes = [
      {x: 80, y: 80, w: 120, h: 100},
      {x: 600, y: 80, w: 120, h: 100},
      {x: 80, y: 420, w: 120, h: 100},
      {x: 600, y: 420, w: 120, h: 100},
      {x: 320, y: 250, w: 160, h: 100}
    ];

    function rectCollide(a, b) {
      return !(a.x + a.size/2 < b.x || a.x - a.size/2 > b.x + b.w ||
               a.y + a.size/2 < b.y || a.y - a.size/2 > b.y + b.h);
    }

    function spawnEnemy() {
      const x = Math.random() * (canvas.width - 100) + 50;
      const y = Math.random() * (canvas.height - 100) + 50;
      enemies.push({
        x: x < 200 ? -40 : canvas.width + 40,
        y: y,
        size: 24,
        speed: 1.65,
        color: '#ff4444',
        health: 65
      });
    }

    function shoot(isSuper = false) {
      const b = brawlers[currentBrawler];
      const now = Date.now();
      if (!isSuper && now - lastShot < 220) return;
      lastShot = now;

      const dx = mouseX - player.x;
      const dy = mouseY - player.y;
      const dist = Math.hypot(dx, dy) || 1;

      bullets.push({
        x: player.x,
        y: player.y,
        vx: (dx / dist) * (isSuper ? 14 : 11),
        vy: (dy / dist) * (isSuper ? 14 : 11),
        size: isSuper ? 14 : 7,
        life: 80,
        damage: isSuper ? b.superDamage : b.damage,
        color: isSuper ? '#00ffff' : '#ffff00',
        isSuper: isSuper
      });

      if (isSuper) {
        superCharge = 0;
        isSuperReady = false;
        superFill.style.width = '0%';
        superText.style.opacity = '0';

        if (currentBrawler === 2) { // Bull - Dash
          const dashSpeed = 18;
          player.x += (dx / dist) * dashSpeed;
          player.y += (dy / dist) * dashSpeed;
        }

        createExplosion(player.x, player.y, '#00ffff', currentBrawler === 0 ? 50 : 35);
      }
    }

    function createExplosion(x, y, color, count = 20) {
      for (let i = 0; i < count; i++) {
        const angle = Math.random() * Math.PI * 2;
        const speed = 3 + Math.random() * 6;
        particles.push({ x, y, vx: Math.cos(angle)*speed, vy: Math.sin(angle)*speed, life: 35, color });
      }
    }

    function startGame() {
      const b = brawlers[currentBrawler];
      player = {
        x: 400, y: 300, size: 28, speed: b.speed,
        color: b.color, health: b.health, angle: 0
      };
      bullets = []; enemies = []; particles = []; score = 0; superCharge = 0; isSuperReady = false;
      scoreDiv.textContent = 'Score: 0';
      superFill.style.width = '0%';
      for (let i = 0; i < 4; i++) spawnEnemy();
      gameLoop();
    }

    function gameLoop() {
      ctx.fillStyle = '#2a5';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Paredes
      ctx.fillStyle = '#1e4d2b';
      ctx.strokeStyle = '#0f2a18';
      ctx.lineWidth = 8;
      walls.forEach(w => {
        ctx.fillRect(w.x, w.y, w.w, w.h);
        ctx.strokeRect(w.x, w.y, w.w, w.h);
      });

      // Arbustos
      ctx.fillStyle = '#1e7d3b';
      ctx.globalAlpha = 0.85;
      bushes.forEach(b => ctx.fillRect(b.x, b.y, b.w, b.h));
      ctx.globalAlpha = 1;

      // Movimento do jogador
      let dx = 0, dy = 0;
      if (keys['w'] || keys['arrowup']) dy -= 1;
      if (keys['s'] || keys['arrowdown']) dy += 1;
      if (keys['a'] || keys['arrowleft']) dx -= 1;
      if (keys['d'] || keys['arrowright']) dx += 1;
      if (joystickActive) { dx += joystickX; dy += joystickY; }

      if (dx || dy) {
        const len = Math.hypot(dx, dy);
        let newX = player.x + (dx / len) * player.speed;
        let newY = player.y + (dy / len) * player.speed;

        let canX = true, canY = true;
        const testX = {x: newX, y: player.y, size: player.size};
        const testY = {x: player.x, y: newY, size: player.size};

        // Colisão com paredes
        walls.forEach(w => {
          if (rectCollide(testX, w)) canX = false;
          if (rectCollide(testY, w)) canY = false;
        });

        if (canX) player.x = newX;
        if (canY) player.y = newY;

        // Manter dentro da tela
        player.x = Math.max(player.size/2, Math.min(canvas.width - player.size/2, player.x));
        player.y = Math.max(player.size/2, Math.min(canvas.height - player.size/2, player.y));
      }

      // Ângulo do jogador (aponta para o mouse)
      const dxMouse = mouseX - player.x;
      const dyMouse = mouseY - player.y;
      player.angle = Math.atan2(dyMouse, dxMouse);

      // Desenhar jogador
      ctx.save();
      ctx.translate(player.x, player.y);
      ctx.rotate(player.angle);
      ctx.fillStyle = player.color;
      ctx.beginPath();
      ctx.arc(0, 0, player.size/2, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = '#111';
      ctx.fillRect(10, -7, 20, 14); // arma
      ctx.restore();

      // Balas
      for (let i = bullets.length - 1; i >= 0; i--) {
        const b = bullets[i];
        b.x += b.vx;
        b.y += b.vy;
        b.life--;

        ctx.fillStyle = b.color;
        ctx.beginPath();
        ctx.arc(b.x, b.y, b.size, 0, Math.PI * 2);
        ctx.fill();

        if (b.isSuper) {
          ctx.strokeStyle = '#ffffff';
          ctx.lineWidth = 3;
          ctx.beginPath();
          ctx.arc(b.x, b.y, b.size + 5, 0, Math.PI * 2);
          ctx.stroke();
        }

        if (b.life <= 0) { bullets.splice(i, 1); continue; }

        let hitWall = false;
        walls.forEach(w => { if (rectCollide(b, w)) hitWall = true; });
        if (hitWall) { bullets.splice(i, 1); continue; }
      }

      // Inimigos
      for (let i = enemies.length - 1; i >= 0; i--) {
        const e = enemies[i];
        const edx = player.x - e.x;
        const edy = player.y - e.y;
        const dist = Math.hypot(edx, edy) || 1;
        e.x += (edx / dist) * e.speed;
        e.y += (edy / dist) * e.speed;

        ctx.fillStyle = e.color;
        ctx.beginPath();
        ctx.arc(e.x, e.y, e.size/2, 0, Math.PI * 2);
        ctx.fill();

        // olhos
        ctx.fillStyle = '#fff';
        ctx.beginPath();
        ctx.arc(e.x-6, e.y-5, 5, 0, Math.PI*2);
        ctx.arc(e.x+6, e.y-5, 5, 0, Math.PI*2);
        ctx.fill();
        ctx.fillStyle = '#000';
        ctx.beginPath();
        ctx.arc(e.x-6 + (edx/dist)*3, e.y-5 + (edy/dist)*3, 2.5, 0, Math.PI*2);
        ctx.arc(e.x+6 + (edx/dist)*3, e.y-5 + (edy/dist)*3, 2.5, 0, Math.PI*2);
        ctx.fill();

        // colisão com jogador
        if (Math.hypot(player.x - e.x, player.y - e.y) < player.size/2 + e.size/2) {
          player.health -= 1.2;
          createExplosion(e.x, e.y, '#ff0000', 15);
          enemies.splice(i, 1);
          spawnEnemy();
        }
      }

      // Colisão bala × inimigo
      for (let i = bullets.length - 1; i >= 0; i--) {
        const b = bullets[i];
        for (let j = enemies.length - 1; j >= 0; j--) {
          const e = enemies[j];
          if (Math.hypot(b.x - e.x, b.y - e.y) < b.size + e.size/2) {
            e.health -= b.damage;
            createExplosion(b.x, b.y, '#ffff88', 10);
            bullets.splice(i, 1);

            if (e.health <= 0) {
              score += 10;
              scoreDiv.textContent = `Score: ${score}`;
              createExplosion(e.x, e.y, '#ff8800', 30);
              enemies.splice(j, 1);
              spawnEnemy();

              superCharge = Math.min(100, superCharge + (b.isSuper ? 40 : 14));
              if (superCharge >= 100 && !isSuperReady) {
                isSuperReady = true;
                superText.style.opacity = '1';
              }
              superFill.style.width = superCharge + '%';
            }
            break;
          }
        }
      }

      // Partículas
      for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i];
        p.x += p.vx;
        p.y += p.vy;
        p.life--;
        p.vx *= 0.95;
        p.vy *= 0.95;

        ctx.globalAlpha = p.life / 35;
        ctx.fillStyle = p.color;
        ctx.fillRect(p.x-3, p.y-3, 6, 6);
        if (p.life <= 0) particles.splice(i, 1);
      }
      ctx.globalAlpha = 1;

      // Game Over
      if (player.health <= 0) {
        ctx.fillStyle = 'rgba(0,0,0,0.75)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#ff4444';
        ctx.font = 'bold 70px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('GAME OVER', canvas.width/2, canvas.height/2 - 20);

        ctx.fillStyle = '#fff';
        ctx.font = '30px Arial';
        ctx.fillText(`Score: ${score}`, canvas.width/2, canvas.height/2 + 50);

        ctx.font = '24px Arial';
        ctx.fillText('Clique para voltar ao menu', canvas.width/2, canvas.height/2 + 100);
        return;
      }

      requestAnimationFrame(gameLoop);
    }

    // ==================== CONTROLES ====================

    window.addEventListener('keydown', e => keys[e.key.toLowerCase()] = true);
    window.addEventListener('keyup',   e => keys[e.key.toLowerCase()] = false);

    canvas.addEventListener('mousemove', e => {
      const rect = canvas.getBoundingClientRect();
      mouseX = e.clientX - rect.left;
      mouseY = e.clientY - rect.top;
    });

    canvas.addEventListener('click', () => { if (player && player.health > 0) shoot(false); });

    // Super com botão direito ou Espaço
    canvas.addEventListener('contextmenu', e => { e.preventDefault(); if (isSuperReady) shoot(true); });
    window.addEventListener('keydown', e => {
      if (e.key === ' ' && isSuperReady) { e.preventDefault(); shoot(true); }
    });

    // Touch controls
    const joystick = document.getElementById('joystick');
    let touchID = null;

    canvas.addEventListener('touchstart', e => {
      for (let t of e.changedTouches) {
        const rect = canvas.getBoundingClientRect();
        const tx = t.clientX - rect.left;
        const ty = t.clientY - rect.top;

        if (tx < 250 && ty > 400) {
          // Joystick
          joystick.style.display = 'block';
          joyCenterX = t.clientX;
          joyCenterY = t.clientY;
          joystick.style.left = (joyCenterX - 65) + 'px';
          joystick.style.top  = (joyCenterY - 65) + 'px';
          joystickActive = true;
          touchID = t.identifier;
        } else if (tx > canvas.width - 200 && ty > canvas.height - 200) {
          // Fire
          if (isSuperReady) shoot(true);
          else shoot(false);
        }
      }
    });

    window.addEventListener('touchmove', e => {
      if (!joystickActive) return;
      for (let t of e.changedTouches) {
        if (t.identifier === touchID) {
          let dx = t.clientX - joyCenterX;
          let dy = t.clientY - joyCenterY;
          const dist = Math.hypot(dx, dy);
          const max = 55;
          if (dist > max) { dx = (dx/dist)*max; dy = (dy/dist)*max; }
          joystickX = dx / max;
          joystickY = dy / max;
          joystick.style.transform = `translate(${dx}px, ${dy}px)`;
        }
      }
    });

    window.addEventListener('touchend', e => {
      for (let t of e.changedTouches) {
        if (t.identifier === touchID) {
          joystickActive = false;
          joystick.style.display = 'none';
          joystick.style.transform = 'translate(0,0)';
          joystickX = joystickY = 0;
          touchID = null;
        }
      }
    });

    // Reiniciar após Game Over
    canvas.addEventListener('click', () => {
      if (player && player.health <= 0) menu.style.display = 'flex';
    });

    console.log("%c🎮 Brawl Stars Mini pronto! Divirta-se!", "color:#00ffff; font-size:18px;");
  </script>
</body>
</html>