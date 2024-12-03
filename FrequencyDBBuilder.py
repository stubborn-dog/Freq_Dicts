import pandas as pd
from collections import defaultdict
import sqlite3
import math


class FrequencyDBBuilder:
    def __init__(self, data, db_name: str, first_table_name, second_table_name, third_table_name, fourth_table_name):
        self.data = data
        self.db_name = db_name

        self.first_table_name = first_table_name
        self.second_table_name = second_table_name
        self.third_table_name = third_table_name
        self.fourth_table_name = fourth_table_name

        self.general_wordform_freq = defaultdict(int)
        self.general_pos_freq = defaultdict(int)
        self.general_lemma_freq = defaultdict(int)

        self.subsample_wordform_freq = defaultdict(lambda: defaultdict(int))
        self.subsample_pos_freq = defaultdict(lambda: defaultdict(int))
        self.subsample_lemma_freq = defaultdict(lambda: defaultdict(int))

        self._process_data()

    def _process_data(self):
        """Process the data and calculate frequencies."""
        for subsample, words in self.data.items():
            for word, details in words.items():
                lemma = details['lemma']
                pos_tag = details['pos_tag']
                wordforms = details['wordforms']

                for wordform in wordforms:
                    self.general_wordform_freq[wordform] += 1
                    self.subsample_wordform_freq[subsample][wordform] += 1

                self.general_pos_freq[pos_tag] += 1
                self.subsample_pos_freq[subsample][pos_tag] += 1

                self.general_lemma_freq[lemma] += 1
                self.subsample_lemma_freq[subsample][lemma] += 1

    def _calculate_tfidf(self, general_freq, subsample_freq):
        """Calculate TF-IDF for each term."""
        tfidf_scores = defaultdict(dict)
        total_subsamples = len(subsample_freq)

        for subsample, freq_dict in subsample_freq.items():
            for term, count in freq_dict.items():
                tf = count / sum(freq_dict.values())  # Term Frequency
                doc_with_term = sum(1 for subsample_dict in subsample_freq.values() if term in subsample_dict)
                idf = math.log((total_subsamples / (1 + doc_with_term)) + 1)  # Inverse Document Frequency
                tfidf_scores[subsample][term] = tf * idf

        return tfidf_scores

    def _add_tfidf_to_df(self, df, subsample_freq, label):
        tfidf_scores = self._calculate_tfidf(self.general_wordform_freq, subsample_freq)

        for subsample, term_scores in tfidf_scores.items():
            df[f'tfidf_in_{subsample}'] = df[label].map(term_scores).fillna(0)

        return df

    def _create_freq_df(self, general_freq, subsample_freq, label):
        rows = []
        unique_items = set(general_freq.keys())

        for item in unique_items:
            row = {
                label: item,
                'generalfrequency': general_freq[item]
            }

            for subsample in subsample_freq:
                row[f'freq_in_{subsample}'] = subsample_freq[subsample].get(item, 0)

            rows.append(row)

        df = pd.DataFrame(rows)
        return self._add_tfidf_to_df(df, subsample_freq, label)

    def get_tfidf_table(self, general_freq, subsample_freq, label):
        tfidf_scores = self._calculate_tfidf(general_freq, subsample_freq)
        rows = []

        for subsample, term_scores in tfidf_scores.items():
            for term, score in term_scores.items():
                rows.append({
                    'subsample': subsample,
                    label: term,
                    'tfidf_score': score
                })

        return pd.DataFrame(rows)

    def get_wordform_df(self):
        return self._create_freq_df(self.general_wordform_freq, self.subsample_wordform_freq, 'wordform')

    def get_pos_tag_df(self):
        return self._create_freq_df(self.general_pos_freq, self.subsample_pos_freq, 'pos_tag')

    def get_lemma_df(self):
        return self._create_freq_df(self.general_lemma_freq, self.subsample_lemma_freq, 'lemma')

    def get_lemma_tfidf_table(self):
        return self.get_tfidf_table(self.general_lemma_freq, self.subsample_lemma_freq, 'lemma')

    def build_freq_db(self):
        conn = sqlite3.connect(self.db_name)
        self.get_lemma_df().to_sql(self.first_table_name, conn, if_exists='replace', index=False)
        self.get_pos_tag_df().to_sql(self.second_table_name, conn, if_exists='replace', index=False)
        self.get_wordform_df().to_sql(self.third_table_name, conn, if_exists='replace', index=False)
        self.get_lemma_tfidf_table().to_sql(self.fourth_table_name, conn, if_exists='replace', index=False)