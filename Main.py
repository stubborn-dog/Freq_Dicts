from pymorphy3 import MorphAnalyzer
import argparse
from TextPreprocessor import TextPreprocesser
from FileManager import FileManager
from FrequencyDBBuilder import FrequencyDBBuilder
from SampleManager import SampleManager
from MorphologicalAnalyser import MorphologicalAnalyser


if __name__ == '__main__':
    # argparse = argparse.ArgumentParser() to read
    file_names = ["corpora/Параграфи_3-6_підручника_з_КЛ_Карпіловської (1).txt", "corpora/подкаст.txt"]
    corpora = [FileManager(file_name).read_file() for file_name in file_names]
    normalised_texts = [TextPreprocesser(text).get_normalised_text() for text in corpora]
    general_samples_morph_dicts = []
    for i in range(len(normalised_texts)):
        sub_samples = SampleManager(normalised_texts[i], 10000, 1000).get_sub_samples()
        general_sample_morph_dict = {}
        for i in range(10):
            general_sample_morph_dict[f'subsample_{i + 1}'] = MorphologicalAnalyser(sub_samples[i]).get_morph_info()
        general_samples_morph_dicts.append(general_sample_morph_dict)
    FrequencyDBBuilder(general_samples_morph_dicts[0], 'samples_stats', 'lemma_stats_book', 'pos_tag_stats_book', 'wordform_stats_book', 'tf_idf_table').build_freq_db()
    FrequencyDBBuilder(general_samples_morph_dicts[1], 'samples_stats', 'lemma_stats_podcast',
                       'pos_tag_stats_podcast', 'wordform_stats_podcast', 'tf_idf_table').build_freq_db()
