import os
import pygame as pg
from Car import Car
from Road import Road
from Visualizer import Visualizer
from utils import fitness, restart_script
from Network import NeuralNetwork


if os.path.exists("./session.txt"):
  with open("./session.txt", "r") as f:
    session_id, mode, file_name = f.read().split(",")
    mode = int(mode)
else:
  exit_code = os.system("python initializing.py")
  if exit_code == 1:
    print("exiting main: error occured when initializing")
    quit()
  else:
    restart_script()

print("session loaded", file_name, mode)
pg.init()

# initialize the pygame window with this size
width, height = 700, 900
screen = pg.display.set_mode((width, height))

# define a road, center is at the middle of width, width is 90% of the road width
road_width = 300
road = Road(road_width / 2, road_width * 0.9)
road_centers = [road.get_lane_center(i) for i in range(road.lanes)]

# layer that all things will be drawn on, it's size is the size of the road
road_render_layer = pg.transform.scale(screen, (road_width, road.lane_height))

# layer that the visualized neural network will use
network_render_layer = pg.Surface((width - road_width, height))


# initalization options, mode corresponds to a menu option
# manual cars
if mode == 1 or mode == 2:
  cars = [Car(
    road.get_lane_center(1), road.lane_height / 2 - 100, 30, 50, max_speed=5, control_mode="man"
  )]

# ai cars
elif mode >= 3:
  cars_amount = 1
  if mode == 4 or mode == 6:
    cars_amount = 100
  cars = Car.generate(cars_amount, road.get_lane_center(1), road.lane_height / 2 - 100, 30, 50)
  best_car = cars[0]
  if NeuralNetwork.has_saved(file_name):
    best_car.brain.load_from_file(file_name)
    for i in range(1, len(cars)):
      cars[i].brain.load_from_file(file_name)
      cars[i].brain.mutate(0.1)
    print("loaded brain")
    best_car.brain.print_formatted()
  else:
    print("no brain found")


# define other cars, at the start of the road in front of car
# endless cars
if mode == 2 or mode == 5 or mode == 6:
  other_cars = Car.generate_dum(road_centers, road.lane_height, amount=80)
# defined cars
else:
  other_cars = [
    Car(road.get_lane_center(1), road.lane_height / 2 - 400, 30, 50, control_mode="dum"),
    Car(road.get_lane_center(0), road.lane_height / 2 - 600, 30, 50, control_mode="dum"),
    Car(road.get_lane_center(2), road.lane_height / 2 - 600, 30, 50, control_mode="dum"),
    Car(road.get_lane_center(0), road.lane_height / 2 - 800, 30, 50, control_mode="dum"),
    Car(road.get_lane_center(1), road.lane_height / 2 - 800, 30, 50, control_mode="dum"),
    Car(road.get_lane_center(1), road.lane_height / 2 - 1000, 30, 50, control_mode="dum"),
    Car(road.get_lane_center(2), road.lane_height / 2 - 1000, 30, 50, control_mode="dum"),
    Car(road.get_lane_center(0), road.lane_height / 2 - 1200, 30, 50, control_mode="dum"),
    Car(road.get_lane_center(1), road.lane_height / 2 - 1200, 30, 50, control_mode="dum"),
  ]


# called every frame
def frame(dt):

  # clear the screen, background
  road_render_layer.fill("lightgray")
  network_render_layer.fill((79, 79, 79))

  # update the cars
  for other_car in other_cars:
    other_car.update(road.borders)
  for car in cars:
    car.update(road.borders, other_cars)
  
  # the best car is the one that went the furthest up and stays in a lane
  car_min_y = min(fitness(car, road_centers) for car in cars)
  global best_car
  best_car = next(filter(lambda car: fitness(car, road_centers) == car_min_y, cars), cars[0])

  # draw the road first so it is under the cars 
  road.render(road_render_layer)
  
  # draw the cars
  for other_car in other_cars:
    other_car.render(road_render_layer, "red")
  for car in cars:
    car.render(road_render_layer, (100, 100, 125))
  
  # draw the best car again, making it stand out
  best_car.render(road_render_layer, "blue", True)

  # draw the neural network
  Visualizer.draw_network(network_render_layer, best_car.brain)

  # put the road layer on the screen on the left side
  # move the render layer as the car moves so the car appears in place
  # the car will be at 70% of the window height
  screen.blit(road_render_layer, (0, -best_car.y_pos + height * 0.7))

  # put the network render layer on the right side of the screen
  screen.blit(network_render_layer, (road_width, 0))



# this function is called every time there is an event
def onEvent(event: pg.event):
  if mode == 1 or mode == 2:
    cars[0].controls.update(event)
  
  if event.type == pg.KEYDOWN:
    # using keys to save a model that looks good
    if event.key == pg.K_z:
      best_car.brain.save_to_file(file_name)
      print("saved brain")
      best_car.brain.print_formatted()
    if event.key == pg.K_x:
      best_car.brain.remove_saved(file_name)
      print("removed brain")

    # using keys to terminate the script and re run for easier reloading
    if event.key == pg.K_r:
      restart_script()
    if event.key == pg.K_q:
      print("quitting session")
      os.remove("./session.txt")
      pg.quit()
      quit()




# clock to limit the fps to 60
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

  # update the screen so things show up
  pg.display.flip()
  dt = clock.tick(60)

# cleanup
print("quitting")
os.remove("./session.txt")
pg.quit()