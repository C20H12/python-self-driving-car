import pygame as pg
from Car import Car
from Road import Road


pg.init()

width, height = 300, 900
screen = pg.display.set_mode((width, height))


road = Road(screen.get_width() / 2, screen.get_width() * 0.9)
render_layer = pg.transform.scale(screen, (width, road.lane_height))

car = Car(road.get_lane_center(1), road.lane_height / 4, 30, 50, max_speed=5)
other_cars = [
  Car(road.get_lane_center(1), road.lane_height / 4 - 300, 30, 50, control_mode="dum")
]

def frame():
  render_layer.fill("lightgray")

  for other_car in other_cars:
    other_car.update(road.borders)
  car.update(road.borders, other_cars)
  
  road.render(render_layer)
  
  for other_car in other_cars:
    other_car.render(render_layer, "red")
  car.render(render_layer, "blue")


  screen.blit(render_layer, (0, -car.y_pos + height * 0.7))


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
  
  frame()

  pg.display.flip()
  clock.tick(60) / 1000

pg.quit()