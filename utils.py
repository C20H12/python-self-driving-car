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
  slope_1 = (line_1_start.y - line_1_end.y) / (line_1_start.x - line_1_end.x)
  slope_2 = (line_2_start.y - line_2_end.y) / (line_2_start.x - line_2_end.x)
  
  slope_diff = slope_1 - slope_2
  if slope_diff == 0:
    return None
  
  intercept_x = (line_2_start.y - slope_2 * line_2_start.x \
                 - line_1_start.y + slope_1 * line_1_start.x) \
                 / (slope_1 - slope_2)
  intercept_y = slope_1 * intercept_x + line_1_start.y - slope_1 * line_1_start.x
  
  line_1_x_bounds = (min(line_1_start.x, line_1_end.x), max(line_1_start.x, line_1_end.x))
  line_1_y_bounds = (min(line_1_start.y, line_1_end.y), max(line_1_start.y, line_1_end.y))
  line_2_x_bounds = (min(line_2_start.x, line_2_end.x), max(line_2_start.x, line_2_end.x))
  line_2_y_bounds = (min(line_2_start.y, line_2_end.y), max(line_2_start.y, line_2_end.y))

  if intercept_x < line_1_x_bounds[0] or intercept_x > line_1_x_bounds[1] \
    or intercept_x < line_2_x_bounds[0] or intercept_x > line_2_x_bounds[1] \
    or intercept_y < line_1_y_bounds[0] or intercept_y > line_1_y_bounds[1] \
    or intercept_y < line_2_y_bounds[0] or intercept_y > line_2_y_bounds[1]:
    return None
  
  return pg.Vector2(intercept_x, intercept_y)

