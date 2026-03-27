const player = document.querySelector('.player');
let posX = 50; // Posição inicial X
let posY = 50; // Posição inicial Y
const velocidade = 10;

document.addEventListener('keydown', (event) => {
    const tecla = event.key.toLowerCase();

    // Movimentação
    if (tecla === 'w' || tecla === 'arrowup') {
        posY -= velocidade;
    }
    if (tecla === 's' || tecla === 'arrowdown') {
        posY += velocidade;
    }
    if (tecla === 'a' || tecla === 'arrowleft') {
        posX -= velocidade;
    }
    if (tecla === 'd' || tecla === 'arrowright') {
        posX += velocidade;
    }

    // Limites do cenário (600px de largura/altura menos o tamanho do player)
    posX = Math.max(0, Math.min(560, posX));
    posY = Math.max(0, Math.min(560, posY));

    // Aplica a nova posição no CSS
    // Nota: No CSS o 'top' controla o eixo Y e 'left' o eixo X
    player.style.left = posX + 'px';
    player.style.top = posY + 'px';
});