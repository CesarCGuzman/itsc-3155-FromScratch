//Note: This was created using a tutorial
// Resource used: https://www.youtube.com/watch?v=y84tBZo8GFo

//Query Selectors
const canvas = document.querySelector("canvas"),
toolBtns = document.querySelectorAll(".tool"),
colorBtns = document.querySelectorAll("#color"),
sizeSlider = document.querySelector(".option #size-slider"),
colorPicker = document.querySelector("#color-picker"),
saveImg = document.querySelector("#post-btn"),
clearCanvas = document.querySelector(".clear"),
fillbtn = document.querySelector(".fill-btn"),
fillcolor = document.querySelector("#fill-color"),
ctx = canvas.getContext("2d");

//Variables and Defaults
let prevMouseX, prevMouseY, snapshot,
selectedTool = "pen",
selectedColor = "#000",
toolsize = 1,
isDrawing = false;

const setCanvasBG = () => {
    // Makes the whole canvas white, solves the issue of our image being transparent
    ctx.fillStyle = "#fff";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = selectedColor; // sets the fillStyle back to selected color
}

window.addEventListener("load", () => {
    //This stops the line from being offset from the mouse
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
    setCanvasBG();
});

// Draws a line from where the user clicks to where user lets go of mouse 
const drawLine = (e) => {
    ctx.beginPath();
    ctx.moveTo(prevMouseX, prevMouseY);
    ctx.lineTo(e.offsetX, e.offsetY); // creates line based on mouse location
    ctx.stroke();
}

/*Draws rectangle/square based on where one clicked to where one
  drags the cursor */
const drawRect = (e) => {
    if(!fillcolor.checked) {
        ctx.strokeRect(e.offsetX, e.offsetY, prevMouseX - e.offsetX, prevMouseY - e.offsetY);
    } else { // Fill is checked so we fill it in with the selected color
        ctx.fillRect(e.offsetX, e.offsetY, prevMouseX - e.offsetX, prevMouseY - e.offsetY);
    }
}

//Draws circle
const drawCircle = (e) => {
    ctx.beginPath();
    // getting radius for circle based on location of mouse pointer
    let radius = Math.sqrt(Math.pow((prevMouseX - e.offsetX), 2) + Math.pow((prevMouseY - e.offsetY), 2));
    ctx.arc(prevMouseX, prevMouseY, radius, 0, 2 * Math.PI);
    ctx.stroke();

    // If fill is checked - Fill it in with selected color
    if(fillcolor.checked) {
        ctx.fill();
        ctx.stroke();
    }
}

//Draws triangle
const drawTriangle = (e) => {
    ctx.beginPath();
    ctx.moveTo(prevMouseX, prevMouseY);
    ctx.lineTo(e.offsetX, e.offsetY); // creates first line based on mouse location
    ctx.lineTo(prevMouseX * 2 - e.offsetX, e.offsetY); // creates bottom line on triangle
    ctx.closePath(); // Closes path of triangle to draw third line
    ctx.stroke();
    
    // Fills if fill is checked
    if(fillcolor.checked) {
        ctx.fill();
        ctx.stroke();
    }
}


const startDrawing = (e) => {
    isDrawing = true;
    prevMouseX = e.offsetX;
    prevMouseY = e.offsetY;
    ctx.beginPath(); // Creates new drawing path, so that when you click the line starts where you click and does not draw to you
    ctx.lineWidth = toolsize;
    ctx.strokeStyle = selectedColor;
    ctx.fillStyle = selectedColor;

    // avoids dragging shape img
    snapshot = ctx.getImageData(0, 0, canvas.width, canvas.height);
}

const drawing = (e) => {
    if(!isDrawing) return; // isDrawing is only set to true when we click - if not, we do not draw
    ctx.putImageData(snapshot, 0, 0);
    if(selectedTool === "pen" || selectedTool === "eraser") {
        ctx.strokeStyle = selectedTool === "eraser" ? "#fff" : selectedColor; // if we select the eraser we set the stroke to white
        ctx.lineTo(e.offsetX, e.offsetY);
        ctx.stroke();
    } else if(selectedTool === 'line'){
        drawLine(e);
    } else if(selectedTool === 'square') {
        drawRect(e);
    } else if(selectedTool === 'circle') {
        drawCircle(e);
    } else if(selectedTool === 'triangle') {
        drawTriangle(e);
    } else {
        fillColor(e);
    }
}

/*Listens for click on all tool buttons (Excludes slider)
  Adds class to selected tool
  Selects tool via id in javascript */
toolBtns.forEach(btn => {
    btn.addEventListener("click", () => {// click event for all the tools
        selectedTool = btn.id;
        document.querySelector(".option .btn-picked").classList.remove("btn-picked");
        btn.classList.add("btn-picked");

        //Shows you what tool you clicked on
        console.log("Tool selected: " + selectedTool);
    });
});

// Changes the size of the tool - Affects shapes as well
sizeSlider.addEventListener("input", () => {
    toolsize = sizeSlider.value;
    var span = document.querySelector(".size-display"); //Gets span element from size slider label
    span.innerHTML = toolsize;                          // Changes the display value to the current tool size

    /*Shows in console the current size of your tool
      commented out as now it updates in real time and
      this can cause it to spam the console */
    //console.log(toolsize);
});

// Changes the color selected - Affects shapes as well
colorBtns.forEach(btn => {
    btn.addEventListener("click", () => {
        //Removes active from currently selected - adds it to the btn we clicked
        document.querySelector(".color-container .selected").classList.remove("selected");
        btn.classList.add("selected");
        selectedColor = btn.value;
        //Shows in console the color selected
        console.log("Color Button clicked: " + selectedColor);
    });
});

/* Changes the color of tool based on selected color
   Also updates background of button for more clarity */
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


// This currently gives me the image in base64 in the console - I'm adding to it to see if we can send that data to flask
// Comment out if you need to test the drawing function as it currently breaks the js
saveImg.addEventListener("click", () => {
    let image = canvas.toDataURL("image/jpeg", 1.0);
    let caption = document.getElementById('caption');
    let captionText = caption.value;    
    data= {
        image_uri: image,
        caption: captionText
    },
    console.log(data);
    fetch(`${window.origin}/compose/scratch/post`, { //Where we want to send the data + where we are located (assumption)
        method: "POST",
        body: JSON.stringify(data),
        cache: "no-cache",
        headers: new Headers({
            "Content-Type": "application/json"
        })
    });
});

/* Should turn the mouse cursor into the selected tool and size when we enter the canvas
   Currently only does the following:
   -    Changes mouse cursor to selected tool

   TODO: Add a way to see the size of the tool
*/
canvas.addEventListener('mouseenter', () => {
    if(selectedTool === 'pen'){
        document.body.style.cursor = "url('/static/icons/pencil.svg') 0 20, move"; // Uses an svg to replace mouse cursor
    }else if(selectedTool === 'eraser') {
        document.body.style.cursor = "url('/static/icons/eraser.svg') 0 20, auto";
    }else if(selectedTool === 'line') {
        document.body.style.cursor = "url('/static/icons/line.svg') 0 20, auto";
    }else if(selectedTool === 'square') {
        document.body.style.cursor = "url('/static/icons/square.svg') 0 20, auto";
    }else if(selectedTool === 'circle') {
        document.body.style.cursor = "url('/static/icons/circle.svg') 0 20, auto";
    }else if(selectedTool === 'triangle') {
        document.body.style.cursor = "url('/static/icons/triangle.svg') 0 20, auto";
    }else {
        document.body.style.cursor = 'default'
    }
});

// This just makes the fill color button a different color when it is checked
fillbtn.addEventListener("change", () => {
    if(fillcolor.checked) {
        console.log("Fill color: Checked");
        document.querySelector(".fill-btn").classList.add("fill-btn-checked");
    } else if(!fillcolor.checked) {
        console.log("Fill color: Unchecked")
        document.querySelector(".fill-btn").classList.remove("fill-btn-checked");
    }
});

clearCanvas.addEventListener("click", () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height); // Clears the whole canvas
});

// Turns the cursor back into default when user leaves the area of the canvas
canvas.addEventListener('mouseleave', () => document.body.style.cursor = 'default');

canvas.addEventListener("mousedown", startDrawing);
canvas.addEventListener("mousemove", drawing);
canvas.addEventListener("mouseup", () => isDrawing = false);