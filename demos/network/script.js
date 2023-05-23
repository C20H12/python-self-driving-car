const netCanvas = document.querySelector("#netCanvas");
netCanvas.width = 500;
netCanvas.height = window.innerHeight;

const ctx = netCanvas.getContext("2d");

ctx.fillStyle = "black";
ctx.fillRect(0, 0, netCanvas.width, netCanvas.height);

const inputArea = document.querySelector("#inputArea");
const inputNodes = document.querySelector("#inputNodes");
inputNodes.addEventListener("input", () => {
  inputArea.innerHTML = "";
  for (let i = 1; i <= inputNodes.valueAsNumber; i++) {
    inputArea.innerHTML += `
      <div>
        <label>Input Value for input node ${i}</label>
        <input type="number" value="0.5" min="0" max="1" step="0.01" class="inputNodeValue">
      </div>
    `;
  }
});

const layersArea = document.querySelector("#layersArea");
const layers = document.querySelector("#layers");
layers.addEventListener("input", () => {
  layersArea.innerHTML = "";
  for (let i = 1; i <= layers.valueAsNumber; i++) {
    layersArea.innerHTML += `
      <div>
        <label>Number of nodes in hidden layer ${i}</label>
        <input type="number" value="1" min="1" step="1" class="layerNodes">
      </div>
    `;
  }
});

const outputArea = document.querySelector("#outputArea");
const outputNodes = document.querySelector("#outputNodes");
outputNodes.addEventListener("input", () => {
  outputArea.innerHTML = "";
  for (let i = 1; i <= outputNodes.valueAsNumber; i++) {
    outputArea.innerHTML += `
      <div>
        <lable>Value of output node ${i}</lable>
        <output class="outputNodeValue"></output>
      </div>
    `;
  }
});
const outputNodeValuesDisp = document.querySelectorAll(".outputNodeValue");

const runBtn = document.querySelector("#run");
runBtn.addEventListener("click", () => {
  ctx.fillStyle = "black"
  ctx.fillRect(0, 0, netCanvas.width, netCanvas.height);

  const inputNodeValues = Array.from(document.querySelectorAll(".inputNodeValue")).map(
    input => input.valueAsNumber
  );
  const layerNodes = Array.from(document.querySelectorAll(".layerNodes")).map(input => input.valueAsNumber);
  const outputNodeValuesDisp = document.querySelectorAll(".outputNodeValue");

  const network = new NeuralNetwork([inputNodeValues.length, ...layerNodes, outputNodeValuesDisp.length]);

  const outputNodeValues = NeuralNetwork.feedForward(inputNodeValues, network);
  for (let i = 0; i < outputNodeValuesDisp.length; i++) {
    outputNodeValuesDisp[i].innerHTML = outputNodeValues[i];
  }

  Visualizer.drawNetwork(ctx, network);
});
