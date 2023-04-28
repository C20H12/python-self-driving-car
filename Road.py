import pygame as pg
from utils import lerp


class Road:
  def __init__(self, x_pos: float, width: float, lanes: int = 3) -> None:
    self.x_pos = x_pos
    self.width = width
    self.lanes = lanes

    self.lane_width = width / lanes
    self.lane_height = 1e4

    self.left_edge = x_pos - width / 2
    self.right_edge = x_pos + width / 2
    self.top = -self.lane_height / 2
    self.bottom = self.lane_height / 2
    
    self.lane_x_positions = [
      lerp(
        self.left_edge, 
        self.right_edge, 
        lane / self.lanes
      ) 
      for lane in range(lanes + 1)
    ]

    self.color = "white"
  
  def getLaneCenter(self, lane_idx: int):
    return self.lane_x_positions[lane_idx % self.lanes] + self.lane_width // 2

  def render(self, screen: pg.Surface):
    for i in range(len(self.lane_x_positions)):
      line_x = self.lane_x_positions[i]
      if i > 0 and i < self.lanes:
        for j in range(int(self.top), int(self.bottom), 50):
          pg.draw.line(screen, self.color, (line_x, j), (line_x, j + 25), 5)
      else:
        pg.draw.line(screen, self.color, (line_x, self.top), (line_x, self.bottom), 5)