const checkBtn = document.getElementById('check-btn');
const userInput = document.getElementById('user-input');
const result = document.getElementById('result');
const canvas = document.getElementById('trace-canvas');
const ctx = canvas.getContext('2d');
const confettiContainer = document.getElementById('confetti-container');

let drawing = false;
let wentOutside = false;
let lastX, lastY;

const letterPath = new Path2D();
letterPath.moveTo(50, 280);
letterPath.lineTo(150, 20);
letterPath.lineTo(250, 280);
letterPath.moveTo(85, 200);
letterPath.lineTo(215, 200);

function drawGuide() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.lineWidth = 40;
    ctx.lineCap = 'round';
    ctx.strokeStyle = '#dddddd';
    ctx.stroke(letterPath);
}

drawGuide();

checkBtn.addEventListener('click', () => {
    const expected = 'El mundo de Sofi';
    if (userInput.value.trim() === expected) {
        result.textContent = '¡Felicidades! Lo has escrito correctamente.';
        result.classList.remove('error');
        result.classList.add('success');
    } else {
        result.textContent = 'Inténtalo de nuevo.';
        result.classList.remove('success');
        result.classList.add('error');
    }
});

canvas.addEventListener('pointerdown', (e) => {
    drawing = true;
    wentOutside = false;
    [lastX, lastY] = [e.offsetX, e.offsetY];
});

canvas.addEventListener('pointermove', (e) => {
    if (!drawing) return;
    const x = e.offsetX;
    const y = e.offsetY;
    ctx.lineWidth = 10;
    ctx.strokeStyle = '#ff69b4';
    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(x, y);
    ctx.stroke();
    [lastX, lastY] = [x, y];

    if (!ctx.isPointInStroke(letterPath, x, y)) {
        wentOutside = true;
    }
});

function finishDrawing() {
    if (!drawing) return;
    drawing = false;
    if (!wentOutside) {
        showConfetti();
    }
}

canvas.addEventListener('pointerup', finishDrawing);
canvas.addEventListener('pointerleave', finishDrawing);

function showConfetti() {
    for (let i = 0; i < 100; i++) {
        const div = document.createElement('div');
        div.className = 'confetti';
        div.style.left = Math.random() * 100 + 'vw';
        div.style.backgroundColor = `hsl(${Math.random() * 360}, 100%, 50%)`;
        div.style.animationDelay = Math.random() * 2 + 's';
        confettiContainer.appendChild(div);
        setTimeout(() => confettiContainer.removeChild(div), 3000);
    }
}
