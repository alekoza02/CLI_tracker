#!/usr/bin/python3

import shutil
import time
import math


class Color:
  def __init__(self, color_index=255):
    self.index = color_index


  def apply_color(self):
    return f"\033[38;5;{self.index}m"


  def set_rgb(self, R=5, G=5, B=5):
    '''Values range from 0 to 5.'''
    self.index = 16 + 36 * R + 6 * G + B
    return f"\033[38;5;{self.index}m"


  def reset(self):
    return f"\033[0m"



class Terminal:

  char_map = {
    "lu" : "╭",
    "ru" : "╮",
    "ld" : "╰",
    "rd" : "╯",
    "vert" : "│",
    "hori" : "─",
  }

  light_map = ".,-~*=!#@$"

  def __init__(self):
    self.update()
    self.reset_canvas()
    self.frame_number = 0
    self.main_color = Color()    


  def update(self):
    self.w, self.h = self.get_size()
    self.aspect_ratio = self.w / self.h


  def get_size(self):
    return shutil.get_terminal_size()


  def clear(self):
    print("\033[2J\033[H", end='', flush=True)


  def render_frame(self):
    self.clear()

    for y in range(self.h):
      if y < self.h - 1:
        print("".join(self.canvas[y]))
      else:
        print("".join(self.canvas[y]), end="", flush=True)


  def insert_char(self, char, x, y):
    self.canvas[y][x] = char


  def insert_string_horizontal(self, string, x, y):
    for index, char in enumerate(string):
      self.canvas[y][x + index] = char
  
  
  def insert_string_vertical(self, string, x, y):
    for index, char in enumerate(string):
      self.canvas[y + index][x] = char


  def reset_canvas(self):
    self.canvas = [[" " for i in range(self.w)] for j in range(self.h)]


  def insert_box(self, x, y, w, h):
    self.insert_char(self.char_map["lu"], x, y)
    self.insert_char(self.char_map["ld"], x, y + h)
    self.insert_char(self.char_map["rd"], x + w, y + h)
    self.insert_char(self.char_map["ru"], x + w, y)

    self.insert_string_horizontal(self.char_map["hori"] * (w - 1), x + 1, y)
    self.insert_string_horizontal(self.char_map["hori"] * (w - 1), x + 1, y + h)
    self.insert_string_vertical(self.char_map["vert"] * (h - 1), x, y + 1)
    self.insert_string_vertical(self.char_map["vert"] * (h - 1), x + w, y + 1)
    

  def insert_colored_frame(self, x, y, w, h, text, color):
    self.insert_box(x, y, w, h)
    self.insert_string_horizontal(text, x + 3, y)
    self.canvas[y][x] = self.main_color.set_rgb(*color) + self.canvas[y][x]
    self.canvas[y + h][x + w] = self.canvas[y + h][x + w] + self.main_color.reset()



  # def insert_concentric_wave(self):
  #   for x in range(self.w):
  #     for y in range(self.h):
  #       light = int(9 * 
  #         (math.sin(
  #             ((x - self.w // 2) / 10) ** 2 + 
  #             ((y * self.aspect_ratio - (self.h // 2) * self.aspect_ratio) / 10) ** 2 +
  #             self.frame_number / 10
  #           ) / 2 + 0.5
  #         )
  #       )
  #       self.insert_char(self.light_map[light], x, y)


  def wait(self, seconds=1):
    time.sleep(seconds)


  def flip(self, fps=60):
    terminal.frame_number += 1
    terminal.render_frame()
    terminal.wait(1 / fps)


if __name__ == "__main__":
  
  terminal = Terminal()

  try:
    while 1:

      terminal.update()
      terminal.reset_canvas()

      terminal.insert_colored_frame(0, 0, terminal.w - 1, 3 * terminal.h // 4 - 1, "Plot section", (0, 5, 5))
      terminal.insert_colored_frame(0, 3 * terminal.h // 4, terminal.w - 1, terminal.h // 4, "Data section", (5, 2, 5))
      
      terminal.flip()
    
  except KeyboardInterrupt:
    terminal.clear()
    print(terminal.main_color.reset())