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
      self.direction -= 1
    elif self.controls.right:
      self.direction += 1

    self.x_pos -= math.sin(self.direction) * self.speed
    self.y_pos -= math.cos(self.direction) * self.speed


  def render(self, screen: pg.Surface):
    surface = pg.Surface((self.width, self.height))
    surface.fill("black")
    surface_rect = surface.get_rect()
    surface_rect.center = (self.width / 2, self.height / 2)
    rotated = pg.transform.rotate(surface, self.direction % 360)
    rotated_rect = rotated.get_rect()
    rotated_rect.center = surface_rect.center
    screen.blit(rotated, rotated_rect)

    