import pygame as pg
from Car import Car


pg.init()

width, height = 300, 900
screen = pg.display.set_mode((width, height))

car = Car(100, 300, 30, 50)

def frame(dt):
  screen.fill("lightgray")

  car.update()
  car.render(screen)

def onEvent(event):
  car.controls.update(event)


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