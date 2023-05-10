const screen = document.querySelector("#screen");
screen.width = window.innerWidth;
screen.height = window.innerHeight;

/**@type {CanvasRenderingContext2D} */
const ctx = screen.getContext("2d");

class Point {
  constructor(x, y, name) {
    this.x = x;
    this.y = y;
    this.name = name;
  }
  draw() {
    ctx.beginPath();
    ctx.fillStyle = "white";
    ctx.arc(this.x, this.y, 8, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
    ctx.fillStyle = "black";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.font = "bold 12px Arial"
    ctx.fillText(this.name, this.x, this.y)
  }
}

const a = new Point(200, 150, 'A');
const b = new Point(150, 250, 'B');
const c = new Point(50, 100, 'C');
const d = new Point(250, 200, 'D');

const points = [
  {pt: a, dragging: false},
  {pt: b, dragging: false},
  {pt: c, dragging: false},
  {pt: d, dragging: false}
];
screen.addEventListener("mousedown", e => {
  for (const point of points) {
    if (e.x < point.pt.x + 10 && 
        e.x > point.pt.x - 10 && 
        e.y < point.pt.y + 10 && 
        e.y > point.pt.y - 10) {
      point.dragging = true;
    }
  }
});

screen.addEventListener("mousemove", e => {
  for (const point of points) {
    if (!point.dragging) continue;
    point.pt.x = e.x;
    point.pt.y = e.y;
  }
})

screen.addEventListener("mouseup", e => {
  for (const point of points) {
    if (point.dragging) {
      point.dragging = false;
    }
  }
})

setInterval(() => {
  ctx.clearRect(0, 0, screen.width, screen.height);
  
  ctx.beginPath();

  ctx.moveTo(a.x, a.y);
  ctx.lineTo(b.x, b.y);

  ctx.moveTo(c.x, c.y);
  ctx.lineTo(d.x, d.y);

  ctx.stroke();


  a.draw();
  b.draw();
  c.draw();
  d.draw();
}, 50)