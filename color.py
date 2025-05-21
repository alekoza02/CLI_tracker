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