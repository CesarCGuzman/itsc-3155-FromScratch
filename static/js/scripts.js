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
let prevMouseX, prevMouseY,
selectedTool = "pen",
selectedColor = "#000",
toolsize = 1,
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
    ctx.lineWidth = toolsize;
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
        selectedTool = btn.id;

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