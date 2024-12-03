from ast import Raise
import re

class SampleManager:
  def __init__(self, text: str, length_of_main_sample: int, length_of_sub_samples: int):
    self.__text = text
    self.__length_of_main_sample = length_of_main_sample
    self.__length_of_sub_sample = length_of_sub_samples
    self.__regex_for_ukrainian_words = r"\b[А-Яа-яїЇєЄЮюґҐіІ'`’-]+"

  def __get_words(self, text:str) -> int:
    words = re.findall(self.__regex_for_ukrainian_words, text)
    return words

  def __get_sample(self, text: str, start_index: int, end_index=int) -> str:
    words = self.__get_words(text)
    words_in_sample = words[start_index:end_index]
    sample = ' '.join(words_in_sample)
    return sample

  def get_main_sample(self):
    main_sample = self.__get_sample(self.__text, start_index=0, end_index=self.__length_of_main_sample)
    return main_sample


  def get_sub_samples(self):
      samples = []
      try:
          start_index = 0
          while start_index < self.__length_of_main_sample:
              end_index = start_index + self.__length_of_sub_sample
              if end_index > self.__length_of_main_sample:
                  end_index = self.__length_of_main_sample
              sample = self.__get_sample(self.__text, start_index, end_index)
              samples.append(sample)
              start_index = end_index
      except Exception as error:
          print(f"An error occurred: {error}")
          raise
      return samples
