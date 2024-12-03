import re

class TextPreprocesser:
  def __init__(self, text: str) -> None:
    self.__text = text
    self.__regex_for_ukrainian_words = r"\b[А-Яа-яїЇєЄЮюґҐіІ'`’-]+"
    self.__regex_for_abriviations_and_trasfers_for_another_line = r"[А-ЯЇЄЮҐІ'`’\.-]{2,}|-\s(?=\w)"


  def get_normalised_text(self) -> str:
    text_without_abriviations_and_transfers_for_another_line = re.sub(self.__regex_for_abriviations_and_trasfers_for_another_line, '', self.__text)
    ukrainian_words = re.findall(self.__regex_for_ukrainian_words, text_without_abriviations_and_transfers_for_another_line)
    normalised_text = ' '.join(ukrainian_words)
    return normalised_text