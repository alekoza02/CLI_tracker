#!/usr/bin/python3

import shutil
import time
import math
import argparse


class Color:
  def __init__(self, color_index=255):
    self.index = color_index


  def apply_color(self):
    return f"\033[38;5;{self.index}m"


  def set_rgb(self, R=5, G=5, B=5):
    '''Values range from 0 to 5.'''
    self.index = 16 + 36 * R + 6 * G + B
    return f"\033[38;5;{self.index}m"


  def set_index(self, index):
    self.index = index
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
    self.file_manager = FileManager()   
    self.plot_manager = PlotManager(self)


  def update(self):
    self.w, self.h = self.get_size()
    self.aspect_ratio = self.w / self.h


  def get_size(self):
    return shutil.get_terminal_size()


  def reset(self, clear=False):
    if clear:
      print("\033[2J", end='', flush=True) 
    print("\033[H", end='', flush=True)


  def render_frame(self):
    self.reset()

    # for y in range(self.h):
    #   if y < self.h - 1:
    #     print("".join(self.canvas[y]))
    #   else:
    #     print("".join(self.canvas[y]), end="", flush=True)
    ris = ""
    for y in range(self.h):
      ris += "".join(self.canvas[y])
    print(ris, end='', flush=True)


  def render_plot(self):
    if self.plot_manager.can_plot:
      
      # axis
      self.insert_string_vertical(self.char_map["vert"] * (self.plot_manager.h + 1), self.plot_manager.x - 1, self.plot_manager.y, (2, 5, 5))
      self.insert_string_horizontal(self.char_map["hori"] * (self.plot_manager.w - 4), self.plot_manager.x - 1, self.plot_manager.y + self.plot_manager.h + 1, (2, 5, 5))
      
      # vertical ticks + labels
      self.insert_string_horizontal(f"{Terminal.char_map["ld"]}", self.plot_manager.x - 1, int(self.plot_manager.y + 4 * (self.plot_manager.h + 1) / 4), (2, 5, 5))
      self.insert_string_horizontal(f" 25% {Terminal.char_map["ru"]}", self.plot_manager.x - 6, int(self.plot_manager.y + 3 * (self.plot_manager.h + 1) / 4), (2, 5, 5))
      self.insert_string_horizontal(f" 50% {Terminal.char_map["ru"]}", self.plot_manager.x - 6, int(self.plot_manager.y + 2 * (self.plot_manager.h + 1) / 4), (2, 5, 5))
      self.insert_string_horizontal(f" 75% {Terminal.char_map["ru"]}", self.plot_manager.x - 6, int(self.plot_manager.y + 1 * (self.plot_manager.h + 1) / 4), (2, 5, 5))
      self.insert_string_horizontal(f"100% {Terminal.char_map["ru"]}", self.plot_manager.x - 6, self.plot_manager.y, (2, 5, 5))
      
      # horizontal labels
      self.insert_string_horizontal(self.plot_manager.x_labels[0], + self.plot_manager.x - 2, self.plot_manager.y + self.plot_manager.h + 2, (2, 5, 5))
      self.insert_string_horizontal(self.plot_manager.x_labels[1], 1 - len(self.plot_manager.x_labels[1]) + int(self.plot_manager.x - 2 + 1 * (self.plot_manager.w - 4) / 4), self.plot_manager.y + self.plot_manager.h + 2, (2, 5, 5))
      self.insert_string_horizontal(self.plot_manager.x_labels[2], 1 - len(self.plot_manager.x_labels[2]) + int(self.plot_manager.x - 2 + 2 * (self.plot_manager.w - 4) / 4), self.plot_manager.y + self.plot_manager.h + 2, (2, 5, 5))
      self.insert_string_horizontal(self.plot_manager.x_labels[3], 1 - len(self.plot_manager.x_labels[3]) + int(self.plot_manager.x - 2 + 3 * (self.plot_manager.w - 4) / 4), self.plot_manager.y + self.plot_manager.h + 2, (2, 5, 5))
      self.insert_string_horizontal(self.plot_manager.x_labels[4], 1 - len(self.plot_manager.x_labels[4]) + int(self.plot_manager.x - 2 + 4 * (self.plot_manager.w - 4) / 4), self.plot_manager.y + self.plot_manager.h + 2, (2, 5, 5))

      # horizontal ticks
      self.insert_string_horizontal(f"{Terminal.char_map["ru"]}", int(self.plot_manager.x - 2 + 2), self.plot_manager.y + self.plot_manager.h + 1, (2, 5, 5))
      self.insert_string_horizontal(f"{Terminal.char_map["ru"]}", int(self.plot_manager.x - 2 + 1 * (self.plot_manager.w - 4) / 4), self.plot_manager.y + self.plot_manager.h + 1, (2, 5, 5))
      self.insert_string_horizontal(f"{Terminal.char_map["ru"]}", int(self.plot_manager.x - 2 + 2 * (self.plot_manager.w - 4) / 4), self.plot_manager.y + self.plot_manager.h + 1, (2, 5, 5))
      self.insert_string_horizontal(f"{Terminal.char_map["ru"]}", int(self.plot_manager.x - 2 + 3 * (self.plot_manager.w - 4) / 4), self.plot_manager.y + self.plot_manager.h + 1, (2, 5, 5))
      self.insert_string_horizontal(f"{Terminal.char_map["ru"]}", int(self.plot_manager.x - 2 + 4 * (self.plot_manager.w - 4) / 4), self.plot_manager.y + self.plot_manager.h + 1, (2, 5, 5))

      # More nuanced ASCII shading based on proximity to integer coordinates
      for x, y in self.plot_manager.screen_data:
        dx_floor = x - math.floor(x)
        dx_ceil = math.ceil(x) - x
        dy_floor = y - math.floor(y)
        dy_ceil = math.ceil(y) - y

        # Minimum distance from integer grid
        min_dx = min(dx_floor, dx_ceil)
        min_dy = min(dy_floor, dy_ceil)
        dist = math.hypot(min_dx, min_dy)

        # Define characters from light to dark for smooth gradation
        shades = " .:-=+*#%@"

        # Normalize distance to an index in shades (0=closest point, highest index=furthest)
        max_dist = math.sqrt(2) / 2  # maximum distance to nearest grid point
        shade_index = int((dist / max_dist) * (len(shades) - 1))
        shade_char = shades[shade_index]

        terminal.insert_char(f"{self.main_color.set_rgb(3, 5, 5)}{shade_char}", int(round(x)), int(round(y)))

      # points = self.plot_manager.screen_data
      # color_code = self.main_color.set_rgb(3, 5, 5)

      # for i, (x, y) in enumerate(points):
      #   x_int, y_int = int(x), int(y)
        
      #   if i < len(points) - 1:
      #     x_next, y_next = points[i + 1]
      #     dx = x_next - x
      #     dy = y_next - y
          
      #     angle = math.atan2(dy, dx)
      #     deg = math.degrees(angle)
          
      #     # Assign character by angle
      #     if -22.5 <= deg < 22.5:
      #       char = '-'
      #     elif 22.5 <= deg < 67.5:
      #       char = '\\'
      #     elif 67.5 <= deg < 112.5 or -112.5 <= deg < -67.5:
      #       char = '|'
      #     elif -67.5 <= deg < -22.5:
      #       char = '/'
      #     else:
      #       char = '*'
      #   else:
      #     char = '*'  # last point marker

      #   terminal.insert_char(f"{color_code}{char}", x_int, y_int)


  def send_error(self, message, x, y):
    x_pos = x - len(message) // 2
    self.insert_string_horizontal(message, x_pos, y, (5, 3, 3))


  def insert_char(self, char, x, y, color=(5, 5, 5)):
    try:
      self.canvas[y][x] = self.main_color.set_rgb(*color) + char + self.main_color.reset()
    except IndexError:
      ...


  def insert_string_horizontal(self, string, x, y, color=(5, 5, 5)):
    try:
      for index, char in enumerate(string):
        self.canvas[y][x + index] = self.main_color.set_rgb(*color) + char
      self.canvas[y][x + len(string) - 1] += self.main_color.reset()
    except IndexError:
      ...


  def insert_string_vertical(self, string, x, y, color=(5, 5, 5)):
    try:
      for index, char in enumerate(string):
        self.canvas[y + index][x] = self.main_color.set_rgb(*color) + char
      self.canvas[y + len(string) - 1][x] += self.main_color.reset()
    except IndexError:
      ...


  def reset_canvas(self):
    self.canvas = [[" " for i in range(self.w)] for j in range(self.h)]


  def insert_box(self, x, y, w, h, color=(5, 5, 5)):
    # rounded borders
    self.insert_char(self.char_map["lu"], x, y, color)
    self.insert_char(self.char_map["ld"], x, y + h, color)
    self.insert_char(self.char_map["rd"], x + w, y + h, color)
    self.insert_char(self.char_map["ru"], x + w, y, color)

    # quad edges
    self.insert_string_horizontal(self.char_map["hori"] * (w - 1), x + 1, y, color)
    self.insert_string_horizontal(self.char_map["hori"] * (w - 1), x + 1, y + h, color)
    self.insert_string_vertical(self.char_map["vert"] * (h - 1), x, y + 1, color)
    self.insert_string_vertical(self.char_map["vert"] * (h - 1), x + w, y + 1, color)
    

  def insert_colored_frame(self, x, y, w, h, text, color):
    self.insert_box(x, y, w, h, color)
    self.insert_string_horizontal(text, x + 3, y, color)


  def update_data_from_file(self):
    c, m = self.file_manager.load_data_from_file()
    self.plot_manager.set_data(c, m)


  def wait(self, seconds=1):
    time.sleep(seconds)


  def flip(self, fps=60):
    terminal.frame_number += 1
    terminal.render_frame()
    terminal.wait(1 / fps)



class FileManager:
  def __init__(self):
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    
    self.args = parser.parse_args()
  
  
  def open_file(self):
    with open(self.args.file, "r") as f:
        content = f.read()
    return content

  
  def convert_to_array(self, content):
    lines = content.split("\n")
    result = []
    metadata = []

    for line in lines:
      try:
        coordinates = line.split()
        
        if len(coordinates) == 2:
          x = float(coordinates[0])
          y = float(coordinates[1])
          result.append((x, y))

        elif len(coordinates) == 3:
          x = float(coordinates[0])
          y = float(coordinates[1])
          z = float(coordinates[2])
          result.append((x, y, z))

        else:
          raise ValueError

      except ValueError:
        metadata.append(line)
    
    return result, metadata


  def load_data_from_file(self):
    c = self.open_file()
    data, metadata = self.convert_to_array(c)
    return data, metadata


class PlotManager:
  
  def __init__(self, parent):
    self.parent = parent
    self.use_time_x = True
    self.x_labels = []
    self.analytics = {
      'len' : None,
      'current_perc' : 0,
      'x_tracked' : None
    }

    self.set_x_limits()
    self.set_y_limits()
    self.set_x_unit('seconds')
    self.track_last_tail()

    self.interpolator = Interpolator()


  def set_y_limits(self, lower=None, upper=None):
    self.y_lower_limit = lower
    self.y_upper_limit = upper
  
  
  def set_x_limits(self, lower=None, upper=None):
    self.x_lower_limit = lower
    self.x_upper_limit = upper


  def set_data(self, data, metadata=""):
    
    if len(data) > 2 and not self.analytics['tracked_type'] is None:
      
      if self.analytics['tracked_type'] is 'elements':
        self.original = data[-self.analytics['x_tracked']:]

      elif self.analytics['tracked_type'] is 'seconds':
        x_last = data[-1][0]
        x_first = x_last - self.analytics['x_tracked']
        x_list = [x for x, y in data]
        deltas = [abs(x - x_first) for x in x_list]
        index = deltas.index(min(deltas))
        self.original = data[index:]
        self.set_x_limits(max(0, x_first), x_last)
    
    else:
      self.original = data

    self.metadata = metadata
    self.can_plot = True

    self.analytics['len'] = len(data)
    
    if len(self.original) > 1:
      self.normalize_data()
      self.apply_screen_coords()
      self.get_x_labels()
    else:
      self.can_plot = False
      self.parent.send_error("Insufficent points", int(self.w / 2), int(self.h / 2))


  def get_x_labels(self):
    delta = self.max_x - self.min_x

    values = [self.min_x + i * delta / 4 for i in range(5)]
    
    if self.use_time_x:
        if self.max_x < 60:
          self.x_labels = [f"{values[i]:.1f}s" for i in range(5)]
        elif self.max_x < 3600:
          self.x_labels = [f"{values[i] // 60:.0f}m {values[i] % 60:.0f}s" for i in range(5)]
        elif self.max_x < 3600 * 24:
          self.x_labels = [f"{values[i] // 3600:.0f}h {values[i] % 3600 // 60:.0f}m" for i in range(5)]
        else:
          self.x_labels = [f"{values[i] // (3600 * 24):.0f}d {values[i] % (3600 * 24) // 3600:.0f}h" for i in range(5)]
    
    else:
      self.x_labels = [f"{values[i]}" for i in range(5)]
      

  def set_boundaries(self, x, y, w, h):
    self.x = x + 6
    self.y = y
    self.w = w
    self.h = h - 2


  def normalize_data(self):
    min_x, max_x, min_y, max_y = math.inf, -math.inf, math.inf, -math.inf
    self.normalized_data = []

    for x, y in self.original:
      min_x = min(min_x, x)
      max_x = max(max_x, x)
      min_y = min(min_y, y)
      max_y = max(max_y, y)

    self.analytics['current_perc'] = max_y

    if not self.y_lower_limit is None:
      min_y = self.y_lower_limit
    
    if not self.y_upper_limit is None:
      max_y = self.y_upper_limit
    
    if not self.x_lower_limit is None:
      min_x = self.x_lower_limit
    
    if not self.x_upper_limit is None:
      max_x = self.x_upper_limit

    self.max_x, self.min_x, self.max_y, self.min_y = max_x, min_x, max_y, min_y

    delta_x, delta_y = max_x - min_x, max_y - min_y

    for x, y in self.original:
      self.normalized_data.append(((x - min_x) / (delta_x),(y - min_y) / (delta_y) ))


  def apply_screen_coords(self):
    self.screen_data = []

    for x, y in self.normalized_data:
      self.screen_data.append((self.x + (self.w - 6) * x, self.y + self.h * (1 - y)))


  def set_x_unit(self, mode='seconds'):
    if mode == 'seconds':
      self.use_time_x = True

  
  def track_last_tail(self, elements=None, typology=None):
    self.analytics['x_tracked'] = elements
    self.analytics['tracked_type'] = typology


class Interpolator:
  def __init__(self):
    ...




if __name__ == "__main__":
  
  print("\033[?25l")
  terminal = Terminal()
  terminal.plot_manager.set_y_limits(0, 100)

  try:
    while 1:

      terminal.update()
      terminal.reset_canvas()

      x1, y1, x2, y2 = 1, 1, (terminal.w - 2) // 2, int(3 * terminal.h / 4) - 2
      terminal.plot_manager.set_boundaries(x1, y1, x2 - x1, y2 - y1)

      terminal.insert_colored_frame(terminal.w // 2 + 1, 0, terminal.w // 2 - 2, int(3 * terminal.h / 4) - 1, "ETA section", (5, 2, 1))
      terminal.send_error("Under developement", (terminal.w + terminal.w // 2) // 2, (int(3 * terminal.h / 4) - 1) // 2 - 2)

      terminal.insert_colored_frame(0, 0, terminal.w // 2, int(3 * terminal.h / 4) - 1, "Plot section", (0, 2, 4))
      terminal.insert_colored_frame(0, int(3 * terminal.h / 4), terminal.w - 1, int(terminal.h / 4), "Data section", (2, 5, 3))

      terminal.update_data_from_file()
      terminal.render_plot()

      # name and lenght of the file
      terminal.insert_string_horizontal(f"Reporting '{terminal.file_manager.args.file}', with {terminal.plot_manager.analytics["len"]} entries.", 2, int(3 * terminal.h / 4) + 2)
      
      # current progress
      terminal.insert_string_horizontal(f"Current progress: {terminal.plot_manager.analytics['current_perc']:.1f}%", 2, int(3 * terminal.h / 4) + 3)

      # interpolation data
      if len(terminal.plot_manager.original) > 2:
        terminal.insert_string_horizontal(f"ETA: {(terminal.plot_manager.original[-1][0] * 100 / terminal.plot_manager.analytics['current_perc']) - terminal.plot_manager.original[-1][0]:.1f}s", terminal.w // 2, int(3 * terminal.h / 4) + 3)

      # METADATA            
      # for index, stringa in enumerate(terminal.plot_manager.metadata):
      #   terminal.insert_string_horizontal(f"{stringa}", 2, int(3 * terminal.h / 4) + 4 + index)

      terminal.flip()
    
  except KeyboardInterrupt:
    terminal.reset(clear=True)
    print(terminal.main_color.reset())
