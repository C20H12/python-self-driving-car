import pygame as pg
from utils import lerp


class Road:
  def __init__(self, x_pos: float, width: float, lanes: int = 3) -> None:
    self.x_pos = x_pos
    self.width = width
    self.lanes = lanes

    self.lane_width = width / lanes
    # arbitrary large number to represent infinity, without it being too slow
    self.lane_height = 3e4

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

    self.borders = [
      # (top left, bottom left)
      (pg.Vector2(self.left_edge, self.top), pg.Vector2(self.left_edge, self.bottom)),
      # (top right, bottom right)
      (pg.Vector2(self.right_edge, self.top), pg.Vector2(self.right_edge, self.bottom))
    ]
  
  def get_lane_center(self, lane_idx: int):
    
    return self.lane_x_positions[lane_idx % self.lanes] + self.lane_width // 2

  def render(self, screen: pg.Surface):
    for i in range(1, len(self.lane_x_positions) - 1):
      line_x = self.lane_x_positions[i]
      # draw a dashed line with 50px spacing and 25px in length
      for j in range(int(self.top), int(self.bottom), 50):
        pg.draw.line(screen, self.color, (line_x, j), (line_x, j + 25), 5)
    
    for border in self.borders:
      pg.draw.line(screen, self.color, (border[0].x, border[0].y), (border[1].x, border[1].y), 5)