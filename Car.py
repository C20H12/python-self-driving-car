import pygame as pg
from Controller import Controller
import math
from Sensor import Sensor


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

    self.sensor = Sensor(self, count=3, spread=math.pi / 2)
  
  def update(self, road_borders):
    self._move()
    self.sensor.update(road_borders)

  def _move(self):
    # increase the speed by bit by bit so that it feels smoother
    if self.controls.forward:
      self.speed += self.acceleration
    elif self.controls.back:
      self.speed -= self.acceleration
    
    # set the speed to the max so that is cannot exceed max_speed
    if self.speed > self.max_speed:
      self.speed = self.max_speed
    
    # the reversing speed is slowed down by a factor
    reverse_factor = 2
    if self.speed < -self.max_speed / reverse_factor:
      self.speed = -self.max_speed / reverse_factor
    
    # decrease the speed by bit by bit when forward or back 
    # are not pressed so it slows down smoothly
    if self.speed > 0:
      self.speed -= self.friction
    if self.speed < 0:
      self.speed += self.friction

    # if speed is somehow between friction and -friction, it will vibrate in place
    # fix for that
    if abs(self.speed) < self.friction:
      self.speed = 0

    # only turn if the car is in motion
    if self.speed != 0:
      # flip the left-right controls if the car is reversing
      flip_factor = 1 if self.speed > 0 else -1

      # turn the car to a direction, the car's unit circle is rotation by 90 deg
      if self.controls.left:
        self.direction += 0.03 * flip_factor
      elif self.controls.right:
        self.direction -= 0.03 * flip_factor

    # 0 deg is facing up, so x and y (sin and cos) are switched
    self.x_pos -= math.sin(self.direction) * self.speed
    self.y_pos -= math.cos(self.direction) * self.speed
  
  def render(self, screen: pg.Surface):
    # reference demo https://www.desmos.com/calculator/xe8kjf55gd

    # construct the points for the 4 corners of the car
    center_x = self.x_pos
    center_y = self.y_pos
    offset_x = self.width // 2
    offset_y = self.height // 2
    rect_points = [
      (center_x - offset_x, center_y - offset_y),
      (center_x + offset_x, center_y - offset_y),
      (center_x + offset_x, center_y + offset_y),
      (center_x - offset_x, center_y + offset_y)
    ]

    # need to use negative dir because the Y axis points down
    sin = math.sin(-self.direction)
    cos = math.cos(-self.direction)
    
    for i in range(len(rect_points)):
      point = rect_points[i]
      # point is translated so that the center is at the origin
      # ie, it is at the same location relative to 0,0 as it is relative to the center
      translated_point = (point[0] - self.x_pos, point[1] - self.y_pos)
      # perform rotation with the rotation matrix
      new_x = translated_point[0] * cos - translated_point[1] * sin
      new_y = translated_point[0] * sin + translated_point[1] * cos
      # translate back to original position
      rect_points[i] = (new_x + self.x_pos, new_y + self.y_pos)

    pg.draw.polygon(screen, "black", rect_points)

    self.sensor.render(screen)
    
  def reset(self, x, y):
    self.x_pos = x
    self.y_pos = y
    self.speed = 0
    self.direction = 0