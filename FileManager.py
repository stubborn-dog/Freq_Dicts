class FileManager:
  def __init__(self, file_name):
    self.__file_name = file_name

  def read_file(self) -> str:
    text = str()
    with open(self.__file_name, 'r+', encoding='utf-8') as f:
      lines = f.read()
      text += lines
    return text