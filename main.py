import pygame as pg
from Car import Car
from Road import Road


pg.init()

width, height = 300, 900
screen = pg.display.set_mode((width, height))


road = Road(screen.get_width() / 2, screen.get_width() * 0.9)
car = Car(road.getLaneCenter(1), road.lane_height / 4, 30, 50)


render_layer = pg.transform.scale(screen, (width, road.lane_height))

def frame():
  render_layer.fill("lightgray")

  car.update()
  # print(car.y_pos)

  road.render(render_layer)
  car.render(render_layer)

  screen.blit(render_layer, (0, -car.y_pos + height * 0.7))




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
  
  frame()

  pg.display.flip()
  clock.tick(60) / 1000

pg.quit()