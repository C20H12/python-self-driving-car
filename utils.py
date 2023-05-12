import pygame as pg


def lerp(A: float, B: float, t: float):
  '''
  A - first number
  B - second number
  t - interpolation factor, a number between 0 and 1
  function to get an intermediate value between A and B
  '''
  return A + (B - A) * t

def get_interersection_point(
  line_1_start: pg.Vector2, 
  line_1_end: pg.Vector2, 
  line_2_start: pg.Vector2, 
  line_2_end: pg.Vector2
):
  a = line_1_start
  b = line_1_end
  c = line_2_start
  d = line_2_end

  tTop = (d.x - c.x) * (a.y - c.y) - (d.y - c.y) * (a.x - c.x)
  uTop = (c.y - a.y) * (a.x - b.x) - (c.x - a.x) * (a.y - b.y)

  bottom = (d.y - c.y) * (b.x - a.x) - (d.x - c.x) * (b.y - a.y)

  if bottom == 0:
    return None
  
  t = tTop / bottom;
  u = uTop / bottom;

  if t < 0 or t > 1 or u < 0 or u > 1:
    return None

  return {
    'point': pg.Vector2(
      lerp(a.x, b.x, t),
      lerp(a.y, b.y, t)
    ),
    'offset': t
  }

