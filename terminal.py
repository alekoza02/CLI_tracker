import shutil
import math
import time

from color import Color
from filemanager import FileManager
from plotmanager import PlotManager

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
    self.finished = False
    self.main_color = Color() 
    self.file_manager = FileManager()  

    data_plot_settings = {
      "parent" : self,
      "color" : (3, 5, 5),
      "second_color" : (5, 5, 5),
      "round_y" : 0,
      "measure_unit_y" : "%",
    }

    interpol_plot_settings = {
      "parent" : self,
      "color" : (5, 3, 1),
      "second_color" : (5, 5, 2),
      "round_y" : 1,
      "measure_unit_y" : "s",
    }

    self.data_plot = PlotManager(**data_plot_settings)
    self.interpol_data = []
    self.interpol_plot = PlotManager(**interpol_plot_settings)

    self.start_frame_time = 0
    self.partial_frame_time = 1
    self.total_frame_time = 1


  def update(self):
    self.start_frame_time = time.perf_counter()
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
    
    ris = ""
    for y in range(self.h):
      ris += "".join(self.canvas[y])
    print(ris, end='', flush=True)


  def render_plot(self, which_plot = 'data'):

    match which_plot:
      case 'data':
        plot = self.data_plot
      case 'interpol':
        plot = self.interpol_plot


    if plot.can_plot:
      
      # axis
      self.insert_string_vertical(self.char_map["vert"] * (plot.h + 1), plot.x - 1, plot.y, plot.color)
      self.insert_string_horizontal(self.char_map["hori"] * (plot.w - 4), plot.x - 1, plot.y + plot.h + 1, plot.color)
      
      # vertical ticks + labels
      self.insert_string_horizontal(f"{float(plot.y_labels[0]):>6.{plot.round_y}f}{plot.measure_unit_y}{Terminal.char_map["ld"]}", plot.x - 8, int(plot.y + 4 * (plot.h + 1) / 4), plot.color)
      self.insert_string_horizontal(f"{float(plot.y_labels[1]):>6.{plot.round_y}f}{plot.measure_unit_y}{Terminal.char_map["ru"]}", plot.x - 8, int(plot.y + 3 * (plot.h + 1) / 4), plot.color)
      self.insert_string_horizontal(f"{float(plot.y_labels[2]):>6.{plot.round_y}f}{plot.measure_unit_y}{Terminal.char_map["ru"]}", plot.x - 8, int(plot.y + 2 * (plot.h + 1) / 4), plot.color)
      self.insert_string_horizontal(f"{float(plot.y_labels[3]):>6.{plot.round_y}f}{plot.measure_unit_y}{Terminal.char_map["ru"]}", plot.x - 8, int(plot.y + 1 * (plot.h + 1) / 4), plot.color)
      self.insert_string_horizontal(f"{float(plot.y_labels[4]):>6.{plot.round_y}f}{plot.measure_unit_y}{Terminal.char_map["ru"]}", plot.x - 8, plot.y, plot.color)
      
      # horizontal labels
      self.insert_string_horizontal(plot.x_labels[0], + plot.x - 2, plot.y + plot.h + 2, plot.color)
      self.insert_string_horizontal(plot.x_labels[1], 1 - len(plot.x_labels[1]) + int(plot.x - 2 + 1 * (plot.w - 4) / 4), plot.y + plot.h + 2, plot.color)
      self.insert_string_horizontal(plot.x_labels[2], 1 - len(plot.x_labels[2]) + int(plot.x - 2 + 2 * (plot.w - 4) / 4), plot.y + plot.h + 2, plot.color)
      self.insert_string_horizontal(plot.x_labels[3], 1 - len(plot.x_labels[3]) + int(plot.x - 2 + 3 * (plot.w - 4) / 4), plot.y + plot.h + 2, plot.color)
      self.insert_string_horizontal(plot.x_labels[4], 1 - len(plot.x_labels[4]) + int(plot.x - 2 + 4 * (plot.w - 4) / 4), plot.y + plot.h + 2, plot.color)

      # horizontal ticks
      self.insert_string_horizontal(f"{Terminal.char_map["ru"]}", int(plot.x - 2 + 2), plot.y + plot.h + 1, plot.color)
      self.insert_string_horizontal(f"{Terminal.char_map["ru"]}", int(plot.x - 2 + 1 * (plot.w - 4) / 4), plot.y + plot.h + 1, plot.color)
      self.insert_string_horizontal(f"{Terminal.char_map["ru"]}", int(plot.x - 2 + 2 * (plot.w - 4) / 4), plot.y + plot.h + 1, plot.color)
      self.insert_string_horizontal(f"{Terminal.char_map["ru"]}", int(plot.x - 2 + 3 * (plot.w - 4) / 4), plot.y + plot.h + 1, plot.color)
      self.insert_string_horizontal(f"{Terminal.char_map["ru"]}", int(plot.x - 2 + 4 * (plot.w - 4) / 4), plot.y + plot.h + 1, plot.color)

      # More nuanced ASCII shading based on proximity to integer coordinates
      for coords in plot.screen_data:
        channels = (len(coords) - 1) // 2
        for channel in range(channels):
          self.insert_char(f"{self.main_color.set_rgb(*coords[2 + 2 * channel])}*", int(round(coords[0])), int(round(coords[1 + 2 * channel])))

          if which_plot == 'data':
            self.insert_string_vertical(f"." * (self.data_plot.h - int(round(coords[1])) + 1), int(round(coords[0])), int(round(coords[1])) + 1, coords[2 + 2 * channel])


    
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
    c = self.color_plot(c, self.data_plot.color)
    self.data_plot.set_plot_data(c, m)
    
  
  def color_plot(self, c, color):
    import random
    for i, coords in enumerate(c):
      if len(coords) == 2:
        c[i] = tuple([*coords, color])
    return c


  def update_interpol(self):

    lunghezza_interpol = len(self.interpol_data)
    lunghezza_plot = len(self.data_plot.original)

    delta_elements = lunghezza_plot - lunghezza_interpol

    if delta_elements > 0 and len(self.data_plot.original) > 2 and not self.finished:

      x, y, yerr = [], [], []

      for index, coords in enumerate(self.data_plot.original[-min(max(50, int(len(self.data_plot.original) / 5)), len(self.data_plot.original)):]):
        x.append(coords[0])
        y.append(coords[1])
        yerr.append(1)      # no weight calculation


      # Weighted means
      w_sum = sum(yerr)
      xw_mean = sum(yerr[i] * x[i] for i in range(len(x))) / w_sum
      yw_mean = sum(yerr[i] * y[i] for i in range(len(y))) / w_sum

      # Weighted slope
      num = sum(yerr[i] * (x[i] - xw_mean) * (y[i] - yw_mean) for i in range(len(x)))
      den = sum(yerr[i] * (x[i] - xw_mean) ** 2 for i in range(len(x)))
      m = num / den
      b = yw_mean - m * xw_mean

      total_time = (100 - b) / m

      for i in range(delta_elements):
        self.interpol_data.append((self.data_plot.original[-1][0], total_time, self.interpol_plot.color, total_time - self.data_plot.original[-1][0], self.interpol_plot.second_color))

    elif delta_elements < -1 and len(self.data_plot.original) > 2:
      self.finished = False
      self.interpol_data = []

    # check for finished work
    try:
      if self.data_plot.original[-1][1] == 100 and not self.finished:
        self.finished = True
        self.interpol_data.append((self.data_plot.original[-1][0], self.data_plot.original[-1][0], self.interpol_plot.color, 0, self.interpol_plot.second_color))
    except IndexError:
      ...

    self.interpol_plot.set_plot_data(self.interpol_data, "", channels=2)


  def wait(self, seconds=1):
    time.sleep(seconds)


  def flip(self, fps=60):
    self.frame_number += 1
    self.render_frame()
    self.partial_frame_time = time.perf_counter() - self.start_frame_time
    self.wait(max(0, (1 / fps) - self.partial_frame_time))
    self.total_frame_time = time.perf_counter() - self.start_frame_time

  
  def get_fps(self):
    return self.partial_frame_time, self.total_frame_time