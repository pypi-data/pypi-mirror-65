import os

import toki_pybind as toki


class Toki:
    def __init__(self):
        toki_path = os.path.dirname(__file__)
        config_file_path = os.path.join(toki_path, 'config')
        toki.set_search_paths([config_file_path])
        self.cfg = toki.default_config()
        self.tokenizer = toki.LayerTokenizer(self.cfg)
        self.sentence_splitter = toki.SentenceSplitter(self.tokenizer)

    def get_all_sentences(self, query: str):
        sentences = []
        query_size = len(query)
        break_vector = self.sentence_splitter.get_breaks(query)
        previous_break_position = 0

        for current_position in break_vector:
            current_sentence = query[previous_break_position:current_position].strip(
            )
            sentences.append(current_sentence)
            previous_break_position = current_position

        if query_size != previous_break_position:
            final_sentence = query[previous_break_position:]
            sentences.append(final_sentence)

        return sentences

    def get_all_sentences_tokenized(self, query: str):
        return self.sentence_splitter.get_all_sentences(query)
