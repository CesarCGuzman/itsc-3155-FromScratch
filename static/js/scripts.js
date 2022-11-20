const canvas = document.querySelector("canvas"),
colorBtns = document.querySelectorAll(".color-container .btn"),
ctx = canvas.getContext("2d");

let prevMouseX, prevMouseY,
isDrawing = false;

window.addEventListener("load", () => {
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
});


const startDrawing = (e) => {
    isDrawing = true;
    prevMouseX = e.offsetX;
    prevMouseY = e.offsetY;
    ctx.beginPath();
    ctx.lineWith = 5;
    ctx.strokeStyle = "#000";
    ctx.fillStyle = "#000";
}

const drawing = (e) => {

    if(!isDrawing) return;
    ctx.lineTo(e.offsetX, e.offsetY);
    ctx.stroke();
}

canvas.addEventListener("mousedown", startDrawing);
canvas.addEventListener("mousemove", drawing);
canvas.addEventListener("mouseup", () => isDrawing = false);