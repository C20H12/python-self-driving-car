import pygame as pg
from Car import Car
from Road import Road


pg.init()

# initialize the pygame window with this size
width, height = 300, 900
screen = pg.display.set_mode((width, height))


# define a road, center is at the middle of width, width is 90% of the width
road = Road(screen.get_width() / 2, screen.get_width() * 0.9)

# layer that all things will be drawn on, it's size is the size of the road
render_layer = pg.transform.scale(screen, (width, road.lane_height))

# define a car and other cars, at a quarter of the road
car = Car(road.get_lane_center(1), road.lane_height / 4, 30, 50, max_speed=5)
other_cars = [
  Car(road.get_lane_center(1), road.lane_height / 4 - 300, 30, 50, control_mode="dum")
]

# this function is called every frame
def frame():
  # clear the screen, background
  render_layer.fill("lightgray")

  # update the cars2
  for other_car in other_cars:
    other_car.update(road.borders)
  car.update(road.borders, other_cars)

  # draw the road first so it is under the cars  
  road.render(render_layer)
  
  # draw the cars
  for other_car in other_cars:
    other_car.render(render_layer, "red")
  car.render(render_layer, "blue")

  # move the render layer as the car moves so the car appears in place
  # the car will be at 70% of the window height
  screen.blit(render_layer, (0, -car.y_pos + height * 0.7))

# this function is called every time there is an event
def onEvent(event):
  car.controls.update(event)

# clock to limit the fps to 60
clock = pg.time.Clock()
running = True
while running:
  for event in pg.event.get():
    if event.type == pg.QUIT:
      running = False
    if event:
      onEvent(event)
  
  frame()

  # update the screen so things show up
  pg.display.flip()
  clock.tick(60)


pg.quit()