import pygame as pg
from Controller import Controller
import math


class Car:
  def __init__(self, x_pos, y_pos, width, height) -> None:
    self.x_pos = x_pos
    self.y_pos = y_pos
    self.width = width
    self.height = height
    self.controls = Controller()

    self.speed = 0
    self.acceleration = 0.2
    self.friction = 0.05
    self.max_speed = 3
    self.direction = 0
  
  def update(self):
    if self.controls.forward:
      self.speed += self.acceleration
    elif self.controls.back:
      self.speed -= self.acceleration
    
    if self.speed > self.max_speed:
      self.speed = self.max_speed
    
    reverse_factor = 2
    if self.speed < -self.max_speed / reverse_factor:
      self.speed = -self.max_speed / reverse_factor
    
    if self.speed > 0:
      self.speed -= self.friction
    if self.speed < 0:
      self.speed += self.friction

    if abs(self.speed) < self.friction:
      self.speed = 0

    if self.controls.left:
      self.direction -= 0.03
    elif self.controls.right:
      self.direction += 0.03

    self.x_pos -= math.sin(self.direction) * self.speed
    self.y_pos -= math.cos(self.direction) * self.speed


  def render(self, screen: pg.Surface):
    offset_x = self.width // 2
    offset_y = self.height // 2
    rect_points = [
      [self.x_pos - offset_x, self.y_pos - offset_y],
      [self.x_pos + offset_x, self.y_pos - offset_y],
      [self.x_pos + offset_x, self.y_pos + offset_y],
      [self.x_pos - offset_x, self.y_pos + offset_y]
    ]
    rect_points_new = []
    sine = math.sin(self.direction)
    cosine = math.cos(self.direction)
    for point in rect_points:
      point_origin = [point[0] - self.x_pos, point[1] - self.y_pos]
      new_x = point_origin[0] * cosine - point_origin[1] * sine
      new_y = point_origin[0] * sine + point_origin[1] * cosine
      rect_points_new.append([new_x + self.x_pos, new_y + self.y_pos])

    pg.draw.polygon(screen, "black", rect_points_new)
    