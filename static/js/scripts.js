const canvas = document.querySelector("canvas"),
toolBtns = document.querySelectorAll(".tool"),
colorBtns = document.querySelectorAll(".color-container .btn"),
ctx = canvas.getContext("2d");

let prevMouseX, prevMouseY,
selectedTool = "pen",
selectedColor = "#000",
isDrawing = false;

window.addEventListener("load", () => {
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
});


const startDrawing = (e) => {
    isDrawing = true;
    prevMouseX = e.offsetX;
    prevMouseY = e.offsetY;
    ctx.beginPath(); // Creates new drwaing path, so that when you click the line starts where you click and does not draw to you
    ctx.lineWith = 5;
    ctx.strokeStyle = selectedColor;
    ctx.fillStyle = selectedColor;
}

const drawing = (e) => {

    if(!isDrawing) return;
    if(selectedTool === "pen" || selectedTool === "eraser") {
        ctx.strokeStyle = selectedTool === "eraser" ? "#fff" : selectedColor;
        ctx.lineTo(e.offsetX, e.offsetY);
        ctx.stroke();
    }
}

toolBtns.forEach(btn => {
    btn.addEventListener("click", () => {// click event for all the tools
        //Removes active from currently active - adds it to the btn we clicked
        document.querySelector(".options .active").classList.remove("active");
        btn.classList.add("active");
        selectedTool = btn.id;

        //Shows you what tool you clicked on
        console.log(selectedTool);
    });
});


colorBtns.forEach(btn => {
    btn.addEventListener("click", () => {
        //Removes active from currently active - adds it to the btn we clicked
        //document.querySelector(".option .selected").classList.remove("selected");
        //btn.classList.add("selected");
        selectedColor = window.getComputedStyle(btn).getPropertyValue("background-color");
        console.log(selectedColor)
    });
});

canvas.addEventListener("mousedown", startDrawing);
canvas.addEventListener("mousemove", drawing);
canvas.addEventListener("mouseup", () => isDrawing = false);