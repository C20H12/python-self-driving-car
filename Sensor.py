import math
import pygame as pg
from utils import lerp


class Sensor:
  def __init__(self, on_car, count = 3, length = 100, spread = math.pi / 4) -> None:
    self.car = on_car
    self.ray_count = count
    self.ray_len = length
    self.ray_spread = spread
    
    self.rays = []

  def update(self, road_borders):
    self._cast_rays()
  
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
    for ray in self.rays:
      pg.draw.line(screen, "yellow", ray[0], ray[1], 2)