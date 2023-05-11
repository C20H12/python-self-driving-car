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

/**
 * get intersection
 * @param {Point} a - line 1 start
 * @param {Point} b - line 1 end
 * @param {Point} c - line 2 start
 * @param {Point} d - line 2 end
 */
function getIntersect(a, b, c, d) {
  /*
  we can linear interpolate from 1 point to another to find any point on a line
  by using a factor t that is from 0 to 1
  x' = lerp(a.x, b.x, t)
  y' = lerp(a.y, b.y, t)
  
  an intersect between 2 lines is when the interpolated point from one line equals
  an interpolated point on another line
  lerp(a.x, b.x, t) = lerp(c.x, d.x, u)
  lerp(a.y, b.y, t) = lerp(c.y, d.y, u)

  now we need to find the correct t and u values, and use them to get the x and y 
  coords of the intersection, we expand the function like:
  a.x + (b.x - a.x) * t = c.x + (d.x - c.x) * u
  a.y + (b.y - a.y) * t = c.y + (d.y - c.y) * u

  move the c.x and c.y over to the left side:
  a.x - c.x + (b.x - a.x) * t = (d.x - c.x) * u 
  a.y - c.y + (b.y - a.y) * t = (d.y - c.y) * u

  can't divide by d.x - c.x, it may be 0, so we need to use subsitution
  use the 2nd equation and multiply both sides by (d.x - c.x)
  the first equation is unchanged:
  a.x - c.x + (b.x - a.x) * t = (d.x - c.x) * u 
  (d.x - c.x)(a.y - c.y + (b.y - a.y) * t) = (d.y - c.y) * u * (d.x - c.x)

  now there is a (d.x - c.x) * u in the 2nd equation, subsitute:
  (d.x - c.x)(a.y - c.y + (b.y - a.y) * t) = (d.y - c.y) * (a.x - c.x + (b.x - a.x) * t)

  distribute:
  (d.x - c.x) * (a.y - c.y) + (d.x - c.x) * (b.y - a.y) * t = (d.y - c.y) * (a.x - c.x) + (d.y - c.y) * (b.x - a.x) * t

  */
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