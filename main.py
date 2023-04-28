import pygame as pg
from Car import Car
from Road import Road


pg.init()

width, height = 300, 900
screen = pg.display.set_mode((width, height))

road = Road(screen.get_width() / 2, screen.get_width() * 0.9)
car = Car(road.getLaneCenter(1), 300, 30, 50)


def frame(dt):
  screen.fill("lightgray")

  car.update()
  road.render(screen)
  car.render(screen)


def onEvent(event):
  car.controls.update(event)
  if event.type == pg.KEYDOWN and event.key == pg.K_r:
    car.reset(100, 300)


clock = pg.time.Clock()
running = True
dt = 0
while running:
  for event in pg.event.get():
    if event.type == pg.QUIT:
      running = False
    if event:
      onEvent(event)
  
  frame(dt)

  pg.display.flip()
  dt = clock.tick(60) / 1000

pg.quit()