import os
import pygame as pg
from Menu import Menu
from uuid import uuid4
from glob import glob

pg.init()

# a separate windows will be spawned
screen = pg.display.set_mode((700, 700))

# global session id for naming new model files
session_id = str(uuid4())[:8]

# text to display at the top
welcome_text_font = pg.font.SysFont("Arial", 17)
welcome_texts = [
  welcome_text_font.render(
    "WASD to move, Z to save a network, X to delete a network, R to reload windoe, Q to quit.",
    True, "white"
  ),
  welcome_text_font.render(
    "Choose a mode and model to begin: ",
    True, "white"
  ),
  welcome_text_font.render(
    "Use arrow keys to navigate menu, Enter to select, Esc to revert selection",
    True, "white"
  ),
]

# first, only allow control on the mode menu, then allow control on the saves menu
menu_controlling = True
saved_menu_controlling = False
confirm_controlling = False

# initialize vars, these are the vital info that will be saved
global_mode = None
model_file_name = None

# options for setting up, the menu controls these options
def set_global_mode(mode):
  global global_mode
  global menu_controlling
  global saved_menu_controlling
  global confirm_controlling
  global_mode = mode
  # open the saves menu
  menu_controlling = False
  if mode >= 3:
    saved_menu_controlling = True
  else:
    confirm_controlling = True
menu = Menu({
  "1 Manual Mode, Defined": lambda: set_global_mode(1) ,
  "2 Manual Mode, Endless": lambda: set_global_mode(2) ,
  "3 AI Mode, Defined, Testing (1 car)": lambda: set_global_mode(3) ,
  "4 AI Mode, Defined, Training (100 cars)": lambda: set_global_mode(4) ,
  "5 AI Mode, Endless, Testing (1 car)": lambda: set_global_mode(5),
  "6 AI Mode, Endless, Training (100 cars)": lambda: set_global_mode(6),
})

# for ai modes, allow the user to pick a model to load
def set_model(name):
  global model_file_name
  global saved_menu_controlling
  global confirm_controlling
  model_file_name = name
  if name == "new":
    model_file_name = session_id
  saved_menu_controlling = False
  confirm_controlling = True
  print(name)
# map each file name to a function that calls the set_model func
# also the option to use a new file, the session ID will be used when saving
saved_menu_dict = {}
for path in glob("./models/*.json"):
  name = path.split(os.path.sep)[-1].split('.')[0]
  saved_menu_dict[name] = lambda name = name: set_model(name) # hack so the lambda closure captures name
saved_menu_dict["create new..."] = lambda: set_model("new")
saved_menu = Menu(saved_menu_dict)


# define the button
confirm_button = pg.Surface((200, 120))
button_text = pg.font.SysFont("Arial", 16).render("confirm", True, (255, 255, 255))

# define the text renderer for the selected options display
chosen_text = pg.font.SysFont("Arial", 20)

def frame():
  screen.fill("#4a4a4a")

  # render the welcome text, each on a row (pygame has no newlings)
  for i in range(len(welcome_texts)):
    screen.blit(welcome_texts[i], (10, 30 + i * 18))

  # render the menus
  menu.render(screen, 100, 100, 300, 200)
  saved_menu.render(screen, 100, 400, 300, 200)
  
  # render the confirm button, if it is active, draw it with a lighter color
  if confirm_controlling:
    confirm_button.fill((127, 127, 127))
  else:
    confirm_button.fill((0, 0, 0))
  # the "confirm" text
  confirm_button.blit(
    button_text, 
    (confirm_button.get_width() / 2 - button_text.get_width() / 2, 
    confirm_button.get_height() / 2 - button_text.get_height() / 2)
  )
  screen.blit(confirm_button, (450, 300))

  # render the selection text display
  screen.blit(chosen_text.render(f"mode: {global_mode}, model: {model_file_name}", True, "white"), (450, 200))


def onEvent(event):
  global menu_controlling
  global saved_menu_controlling
  global confirm_controlling

  if event.type == pg.KEYDOWN:
    # control the menus or button only when they are activated
    if menu_controlling:
      menu.update_controls(event.key)
      return
    if saved_menu_controlling:
      saved_menu.update_controls(event.key)
      return
    if confirm_controlling:
      # final decision, save to a file and quit
      if event.key == pg.K_RETURN:
        with open("./session.txt", 'w') as f:
          f.write(f"{session_id},{global_mode},{model_file_name}")
        print("saved session")
        print("initializing finished")
        print("quitting initilizing process")
        pg.quit()
        quit()

      
      # reset the active menu, allowing for a reselection
      if event.key == pg.K_ESCAPE:
        menu_controlling = True
        saved_menu_controlling = False
        confirm_controlling = False

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
  
  frame()

  # update the screen so things show up
  pg.display.flip()
  dt = clock.tick(60)

# cleanup
print("aborting initilizing process")
pg.quit()
quit(1)