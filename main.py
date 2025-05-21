#!/usr/bin/python3

from color import Color
from terminal import Terminal
from filemanager import FileManager
from plotmanager import PlotManager


if __name__ == "__main__":
  
  print("\033[?25l")
  terminal = Terminal()
  terminal.interpol_plot.track_last_tail(30, 'seconds')
  
  try:
    while 1:

      terminal.data_plot.set_y_limits(0, 100)
      y_interpol = [min(coords[1], coords[3]) for coords in terminal.interpol_data]
      limite = min(y_interpol) if len(y_interpol) > 2 else 1
      terminal.interpol_plot.set_y_limits(min(0, limite), None)
      
      terminal.update()
      terminal.reset_canvas()

      x1, y1, x2, y2 = 1, 1, (terminal.w - 2) // 2, int(4 * terminal.h / 5) - 2
      terminal.data_plot.set_boundaries(x1, y1, x2 - x1, y2 - y1)
      
      x1, y1, x2, y2 = (terminal.w) // 2 + 2, 1, terminal.w - 3, int(4 * terminal.h / 5) - 2
      terminal.interpol_plot.set_boundaries(x1, y1, x2 - x1, y2 - y1)

      terminal.insert_colored_frame(terminal.w // 2 + 1, 0, terminal.w // 2 - 2, int(4 * terminal.h / 5) - 1, "ETA section", (5, 2, 1))
      terminal.insert_colored_frame(0, 0, terminal.w // 2, int(4 * terminal.h / 5) - 1, "Plot section", (2, 3, 4))
      terminal.insert_colored_frame(0, int(4 * terminal.h / 5), terminal.w - 1, int(terminal.h / 5), "Data section", (2, 5, 3))

      terminal.update_data_from_file()
      terminal.update_interpol()

      terminal.render_plot('data')
      terminal.render_plot('interpol')

      # name and lenght of the file
      terminal.insert_string_horizontal(f"Reporting '{terminal.file_manager.args.file}', with {terminal.data_plot.analytics["len"]} entries.", 2, int(4 * terminal.h / 5) + 2)
      
      # current progress
      terminal.insert_string_horizontal(f"{'Current progress:':<27} {terminal.data_plot.analytics['current_perc']:.1f}%", terminal.w // 2, int(4 * terminal.h / 5) + 2, terminal.data_plot.color)

      # interpolation data
      if len(terminal.interpol_data) > 2:
        terminal.insert_string_horizontal(f"{'TOTAL expected time:':<27} {terminal.interpol_data[-1][1]:.1f}s", terminal.w // 2, int(4 * terminal.h / 5) + 3, terminal.interpol_plot.color)
        terminal.insert_string_horizontal(f"{'ELAPSED time:':<27} {terminal.interpol_data[-1][0]:.1f}s", terminal.w // 2, int(4 * terminal.h / 5) + 4)
        terminal.insert_string_horizontal(f"{'ESTIMATED remaining time:':<27} {terminal.interpol_data[-1][3]:.1f}s", terminal.w // 2, int(4 * terminal.h / 5) + 5, terminal.interpol_plot.second_color)

      rendering_fps, capped_fps = terminal.get_fps()
      terminal.insert_string_horizontal(f"{'Rendering FPS:':<27} {1 / rendering_fps:.0f}", 2, int(4 * terminal.h / 5) + 3)
      terminal.insert_string_horizontal(f"{'Capped FPS:':<27} {1 / capped_fps:.0f}", 2, int(4 * terminal.h / 5) + 4)


      terminal.flip()
    
  except KeyboardInterrupt:
    terminal.reset(clear=True)
    print(terminal.main_color.reset())
