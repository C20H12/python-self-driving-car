import math
import pygame as pg
from utils import lerp, get_interersection_point


class Sensor:
  def __init__(self, on_car, count = 3, length = 100, spread = math.pi / 4) -> None:
    self.car = on_car
    self.ray_count = count
    self.ray_len = length
    self.ray_spread = spread
    
    self.rays = []
    self.readings = []

  def update(self, road_borders):
    self._cast_rays()
    self.readings.clear()
    for ray in self.rays:
      self.readings.append(
        self._get_reading(ray, road_borders)
      )
  
  def _get_reading(self, ray, borders):
    touches = []
    for border in borders:
      intersection = get_interersection_point(
        ray[0],
        ray[1],
        border[0],
        border[1]
      )
      if intersection:
        touches.append(intersection)
    
    if len(touches) == 0:
      return None
    else:
      # closest intersection to the start of the ray (car center)
      min_offset = min(map(lambda t: t['offset'], touches))
      for touch in touches:
        if touch['offset'] == min_offset:
          return touch['point']

  def _cast_rays(self):
    self.rays = []

    for i in range(self.ray_count):
      angle_factor = i / (self.ray_count - 1) if self.ray_count > 1 else 0.5
      angle = lerp(
        self.ray_spread / 2,
        -self.ray_spread / 2,
        angle_factor
      )
      angle += self.car.direction
      start_pos = pg.Vector2(self.car.x_pos, self.car.y_pos)
      end_pos = pg.Vector2(
        self.car.x_pos - math.sin(angle) * self.ray_len, 
        self.car.y_pos - math.cos(angle) * self.ray_len
      )
      self.rays.append((start_pos, end_pos))
  
  def render(self, screen: pg.Surface):
    for i in range(self.ray_count):
      ray_start = self.rays[i][0]
      ray_end = self.rays[i][1]

      if self.readings[i]:
        pg.draw.line(screen, "yellow", ray_start, self.readings[i], 2)
        pg.draw.line(screen, "black", self.readings[i], ray_end, 2)
      else:
        pg.draw.line(screen, "yellow", ray_start, ray_end, 2)
        