//Note: This was created using a tutorial
// Resource used: https://www.youtube.com/watch?v=y84tBZo8GFo

// TODO: line, square, circle, and triangle tools

//Query Selectors
const canvas = document.querySelector("canvas"),
toolBtns = document.querySelectorAll(".tool"),
colorBtns = document.querySelectorAll(".color-container .btn"),
sizeSlider = document.querySelector(".option #size-slider"),
colorPicker = document.querySelector("#color-picker"),
ctx = canvas.getContext("2d");

//Variables and Defaults
let prevMouseX, prevMouseY, snapshot,
selectedTool = "pen",
selectedColor = "#000",
toolsize = 1,
isDrawing = false;

window.addEventListener("load", () => {
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
});


const drawLine = (e) => {
    ctx.beginPath();
    ctx.moveTo(prevMouseX, prevMouseY);
    ctx.lineTo(e.offsetX, e.offsetY); // creates line based on mouse location
    ctx.stroke();
}

//Draws rectangle, if fill is checked it draws a filled in rectangle - technically can be used for squares as well
const drawRect = (e) => {
    ctx.strokeRect(e.offsetX, e.offsetY, prevMouseX - e.offsetX, prevMouseY - e.offsetY);
}

//Draws circle, if fill is checked it draws a filled in circle
const drawCircle = (e) => {
    ctx.beginPath();
    // getting radius for circle based on location of mouse pointer
    let radius = Math.sqrt(Math.pow((prevMouseX - e.offsetX), 2) + Math.pow((prevMouseY - e.offsetY), 2));
    ctx.arc(prevMouseX, prevMouseY, radius, 0, 2 * Math.PI);
    ctx.stroke();
}

//Draws triangle, if fill is checked it draws a filled in triangle
const drawTriangle = (e) => {
    ctx.beginPath();
    ctx.moveTo(prevMouseX, prevMouseY);
    ctx.lineTo(e.offsetX, e.offsetY); // creates first line based on mouse location
    ctx.lineTo(prevMouseX * 2 - e.offsetX, e.offsetY); // creates bottom line on triangle
    ctx.closePath(); // Closes path of triangle to draw third line
    ctx.stroke();
}


const startDrawing = (e) => {
    isDrawing = true;
    prevMouseX = e.offsetX;
    prevMouseY = e.offsetY;
    ctx.beginPath(); // Creates new drwaing path, so that when you click the line starts where you click and does not draw to you
    ctx.lineWidth = toolsize;
    ctx.strokeStyle = selectedColor;
    ctx.fillStyle = selectedColor;

    // avoids dragging shape img
    snapshot = ctx.getImageData(0, 0, canvas.width, canvas.height);
}

const drawing = (e) => {
    if(!isDrawing) return; //Does not draw if not true
    ctx.putImageData(snapshot, 0, 0);
    if(selectedTool === "pen" || selectedTool === "eraser") {
        ctx.strokeStyle = selectedTool === "eraser" ? "#fff" : selectedColor;
        ctx.lineTo(e.offsetX, e.offsetY);
        ctx.stroke();
    } else if(selectedTool === "line"){
        drawLine(e);
    } else if(selectedTool === "square") {
        drawRect(e);
    } else if(selectedTool ==="circle") {
        drawCircle(e);
    } else {
        drawTriangle(e);
    }
}

toolBtns.forEach(btn => {
    btn.addEventListener("click", () => {// click event for all the tools
        selectedTool = btn.id;
        document.querySelector(".option .btn-picked").classList.remove("btn-picked");
        btn.classList.add("btn-picked");

        //Shows you what tool you clicked on
        console.log("Tool selected: " + selectedTool);
    });
});

sizeSlider.addEventListener("change", () => {
    toolsize = sizeSlider.value;

    //Shows in console the current size of your tool
    console.log(toolsize);
});

colorBtns.forEach(btn => {
    btn.addEventListener("click", () => {
        //Removes active from currently selected - adds it to the btn we clicked
        selectedColor = window.getComputedStyle(btn).getPropertyValue("background-color");
        document.querySelector(".color-container .selected").classList.remove("selected");
        btn.classList.add("selected");
        //Shows in console the color selected
        console.log("Color Button clicked: " + selectedColor);
    });
});

colorPicker.addEventListener("change", () => {
    // Sets current color to value selected and changes the color of the button to the selected color
    colorPicker.parentElement.style.background = colorPicker.value;

    //Remove selected class from currently selected and add it to the colorpicker
    document.querySelector(".color-container .selected").classList.remove("selected");
    colorPicker.parentElement.classList.add("selected");
    selectedColor = colorPicker.value;

    //Shows in console the color value
    console.log("Color Picked: " + colorPicker.value);
});

canvas.addEventListener("mousedown", startDrawing);
canvas.addEventListener("mousemove", drawing);
canvas.addEventListener("mouseup", () => isDrawing = false);