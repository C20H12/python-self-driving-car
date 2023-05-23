import pygame as pg
from typing import Dict, Callable, Tuple


class Menu:
  def __init__(self, 
               options_dict: Dict[str, Callable], 
               customizations: Dict[str, Tuple[int,int,int]] = dict()):
    '''
    options_dict: a dictionary of options, the key is the option name and the value is the function to execute
    customizations: a dictionary of customizations, it can contain the following keys:
      bg: the background color of the menu
      text: the text color of the menu
      selected: the background color of the selected option
      selected_text: the text color of the selected option
      font: the font of the text
    '''
    self.functions = list(options_dict.values())
    self.items = list(options_dict.keys())
    self.selected_idx = 0

    # get the customized values, using a default value if the key is not found
    self.bg_color = customizations.get('bg', (0, 0, 0))
    self.text_color = customizations.get('text', (255, 255, 255))
    self.select_color = customizations.get('selected', (127, 127, 127))
    self.select_text_color = customizations.get('selected_text', (0, 0, 0))
    self.font = customizations.get('font', "Arial")

  def render(self, width, height):
    '''
    width: the width of the menu
    height: the height of the menu
    renders the menu to a surface and returns it
    need to blit it to a screen to make it visible
    '''
    surf = pg.Surface((width, height))
    surf.fill(self.bg_color)
    item_height = height / len(self.items)

    for i in range(len(self.items)):
      # render the rect for each item
      # use the selected color is i is selected
      rect_surf = pg.Surface((width, item_height))
      rect_color = self.select_color if i == self.selected_idx else self.bg_color
      rect_surf.fill(rect_color)

      # draw the text using the corresponding text color and font
      text = self.items[i]
      text_color = self.select_text_color if i == self.selected_idx else self.text_color
      text_surf = pg.font.SysFont(self.font, 20).render(text, True, text_color)

      # center the text inside the rect
      text_start = ((rect_surf.get_width() - text_surf.get_width()) / 2, (rect_surf.get_height() - text_surf.get_height()) / 2)
      # draw the text onto the rect
      rect_surf.blit(text_surf, text_start)
      # draw the rect to the surface 
      surf.blit(rect_surf, (0, item_height * i))
    
    return surf

  def update_controls(self, key):
    # only increment if it is not at the end of the list
    if key == pg.K_DOWN and self.selected_idx != len(self.items) - 1:
        self.selected_idx += 1
    # only decrement if it is not 0
    if key == pg.K_UP and self.selected_idx != 0:
      self.selected_idx -= 1
    # run the function when enter is pressed
    if key == pg.K_RETURN:
      self.functions[self.selected_idx]()
