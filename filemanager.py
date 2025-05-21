import argparse

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