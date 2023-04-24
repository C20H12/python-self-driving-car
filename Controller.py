import pygame as pg


class Controller:
  def __init__(self) -> None:
    self.forward = False
    self.back = False
    self.left = False
    self.right = False

  def update(self, event):
    if event.type == pg.KEYDOWN:
      if event.key in (pg.K_UP, pg.K_w):
        self.forward = True
      elif event.key in (pg.K_DOWN, pg.K_s):
        self.back = True
      elif event.key in (pg.K_LEFT, pg.K_a):
        self.left = True
      elif event.key in (pg.K_RIGHT, pg.K_d):
        self.right = True
    elif event.type == pg.KEYUP:
      if event.key in (pg.K_UP, pg.K_w):
        self.forward = False
      elif event.key in (pg.K_DOWN, pg.K_s):
        self.back = False
      elif event.key in (pg.K_LEFT, pg.K_a):
        self.left = False
      elif event.key in (pg.K_RIGHT, pg.K_d):
        self.right = False
