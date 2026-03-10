<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Olá Mundo - Terra Girando NASA</title>
  
  <style>
    body {
      margin: 0;
      height: 100vh;
      background: radial-gradient(circle at center, #0a001f 0%, #000814 100%);
      display: flex;
      justify-content: center;
      align-items: center;
      font-family: Arial, Helvetica, sans-serif;
      overflow: hidden;
    }

    .container {
      position: relative;
      width: min(80vmin, 420px);
      height: min(80vmin, 420px);
      text-align: center;
    }

    .earth-link {
      display: block;
      width: 100%;
      height: 100%;
      cursor: pointer;
      transition: transform 0.3s ease;
    }

    .earth-link:hover {
      transform: scale(1.05); /* leve zoom ao hover pra dar feedback */
    }

    .earth {
      width: 100%;
      height: 100%;
      border-radius: 50%;
      background: url('https://upload.wikimedia.org/wikipedia/commons/7/7f/Rotating_earth_animated_transparent.gif') center/cover no-repeat;
      box-shadow: 
        0 0 80px rgba(80, 160, 255, 0.8),
        inset 0 0 100px rgba(0, 0, 0, 0.7);
    }

    .text {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      color: #00ffff;
      font-size: clamp(2.8rem, 9vw, 5rem);
      font-weight: 900;
      letter-spacing: 5px;
      text-shadow: 
        0 0 10px #00ffff,
        0 0 30px #00ffff,
        0 0 60px #0099ff,
        0 0 100px #0044cc;
      pointer-events: none; /* texto não interfere no clique */
      z-index: 10;
      white-space: nowrap;
      animation: pulse 5s ease-in-out infinite alternate;
    }

    @keyframes pulse {
      from { opacity: 0.8; filter: brightness(1); }
      to   { opacity: 1; filter: brightness(1.3); }
    }

    /* Player invisível do YouTube */
    .audio-player {
      position: absolute;
      opacity: 0;
      pointer-events: none;
      width: 1px;
      height: 1px;
    }
  </style>
</head>
<body>

  <div class="container">
    <a href="https://www.nasa.gov/" target="_blank" class="earth-link">
      <div class="earth"></div>
    </a>
    <div class="text">Olá Mundo</div>
  </div>

  <!-- Embed do YouTube invisível com autoplay e loop (começando em ~30s) -->
  <iframe 
    class="audio-player"
    src="https://www.youtube.com/embed/xS_E7WzPjvE?start=30&autoplay=1&loop=1&playlist=xS_E7WzPjvE&mute=0&controls=0&showinfo=0&rel=0&modestbranding=1"
    frameborder="0" 
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
    allowfullscreen>
  </iframe>

</body>
</html>