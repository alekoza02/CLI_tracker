import math

class PlotManager:
  
  def __init__(self, parent, color, second_color, round_y, measure_unit_y):
    self.parent = parent
    self.use_time_x = True
    self.use_time_y = False
    self.can_plot = False
    self.x_labels = []
    self.y_labels = []
    self.round_y = round_y
    self.measure_unit_y = measure_unit_y
    self.color = color
    self.second_color = second_color
    self.analytics = {
      'len' : None,
      'current_perc' : 0,
      'x_tracked' : None
    }

    self.set_x_limits()
    self.set_y_limits()
    self.set_x_unit('seconds')
    self.track_last_tail()


  def set_y_limits(self, lower=None, upper=None):
    self.y_lower_limit = lower
    self.y_upper_limit = upper
  
  
  def set_x_limits(self, lower=None, upper=None):
    self.x_lower_limit = lower
    self.x_upper_limit = upper


  def set_plot_data(self, data, metadata="", channels=1):
    if len(data) > 2 and not self.analytics['tracked_type'] is None:
      
      if self.analytics['tracked_type'] is 'elements':
        self.original = data[-self.analytics['x_tracked']:]
  
      elif self.analytics['tracked_type'] is 'seconds':
        x_last = data[-1][0]
        x_first = x_last - self.analytics['x_tracked']
        x_list = [coords[0] for coords in data]
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
      self.normalize_data(channels)
      self.apply_screen_coords(channels)
      self.get_x_labels()
      self.get_y_labels()
    else:
      self.can_plot = False
      self.parent.send_error("Insufficent points", self.x + int(self.w / 2), self.y + int(self.h / 2))


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
  
  
  def get_y_labels(self):
    delta = self.max_y - self.min_y

    values = [self.min_y + i * delta / 4 for i in range(5)]
    
    if self.use_time_y:
        if self.max_y < 60:
          self.y_labels = [f"{values[i]:.1f}s" for i in range(5)]
        elif self.max_y < 3600:
          self.y_labels = [f"{values[i] // 60:.0f}m {values[i] % 60:.0f}s" for i in range(5)]
        elif self.max_y < 3600 * 24:
          self.y_labels = [f"{values[i] // 3600:.0f}h {values[i] % 3600 // 60:.0f}m" for i in range(5)]
        else:
          self.y_labels = [f"{values[i] // (3600 * 24):.0f}d {values[i] % (3600 * 24) // 3600:.0f}h" for i in range(5)]
    
    else:
      self.y_labels = [f"{values[i]}" for i in range(5)]
      

  def set_boundaries(self, x, y, w, h):
    self.x = x + 8
    self.y = y
    self.w = w - 2
    self.h = h - 2


  def normalize_data(self, channels=1):
    min_x, max_x, min_y, max_y = math.inf, -math.inf, math.inf, -math.inf
    self.normalized_data = []

    for coords in self.original:
      min_x = min(min_x, coords[0])
      max_x = max(max_x, coords[0])
      min_y = min(min_y, min([coords[i] for i in range(1, 2 * channels, 2)]))
      max_y = max(max_y, max([coords[i] for i in range(1, 2 * channels, 2)]))

    self.analytics['current_perc'] = max_y

    if not self.y_lower_limit is None:
      min_y = self.y_lower_limit
    
    if not self.y_upper_limit is None:
      max_y = self.y_upper_limit
    
    if not self.x_lower_limit is None:
      min_x = self.x_lower_limit
    
    if not self.x_upper_limit is None:
      max_x = self.x_upper_limit

    if min_y == max_y:
      min_y -= 1
      max_y += 1
    
    if min_x == max_x:
      min_x -= 1
      max_x += 1
    
    self.max_x, self.min_x, self.max_y, self.min_y = max_x, min_x, max_y, min_y

    delta_x, delta_y = max_x - min_x, max_y - min_y

    for coords in self.original:
      fin_coords = [(coords[0] - min_x) / (delta_x)]
      for i in range(1, 2 * channels, 2):
        fin_coords.extend([(coords[i] - min_y) / (delta_y), coords[i + 1]])
      
      self.normalized_data.append(tuple(fin_coords))


  def apply_screen_coords(self, channels=1):
    self.screen_data = []

    for coords in self.normalized_data:
      fin_coords = [self.x + (self.w - 6) * coords[0]]
      for i in range(1, 2 * channels, 2):
        fin_coords.extend([self.y + self.h * (1 - coords[i]), coords[i + 1]])
      
      self.screen_data.append(tuple(fin_coords))


  def set_x_unit(self, mode='seconds'):
    if mode == 'seconds':
      self.use_time_x = True

  
  def track_last_tail(self, elements=None, typology=None):
    '''Available modes: `seconds`, `elements`'''
    self.analytics['x_tracked'] = elements
    self.analytics['tracked_type'] = typology