import spacy, re
from spacy.tokenizer import Tokenizer

class MorphologicalAnalyser:
    def __init__(self, text: str):
        self._text = text
        self._spacy_model = 'uk_core_news_lg'
        self._custom_token_pattern = re.compile(r"\b[А-Яа-яїЇєЄЮюґҐіІ'`’-]+")  # Define regex pattern
        self._nlp = spacy.load(self._spacy_model)
        self._nlp.tokenizer.token_match = self._custom_token_match  # Assign custom tokenizer
        self._doc = self._nlp(self._text)  # Process text immediately

    def _custom_token_match(self, text: str):
        return self._custom_token_pattern.match(text)

    def get_morph_info(self):
        morph_info_dict = dict()
        for token in self._doc:
          if token.lemma_ not in morph_info_dict.keys():
            morph_info_dict[token.lemma_] = {'pos_tag': token.pos_, 'lemma': token.lemma_, 'wordforms': []}
          morph_info_dict[token.lemma_]['wordforms'].append(token.text)
        return morph_info_dict