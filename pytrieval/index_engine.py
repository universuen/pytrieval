"""
Definition of IndexEngine
"""
import pickle

from tqdm import tqdm

from pytrieval.database.handler import Handler
from pytrieval.logger import Logger
from pytrieval.utils import tokenize


class IndexEngine:

    def __init__(self, db_handler: Handler):
        self.db_handler = db_handler
        self.db_handler.logger.disabled = True
        self.logger = Logger(self.__class__.__name__)
        self.idx_map = dict()

    def build(self):
        self.logger.info('building index engine from dataset')
        # load all news from the database
        for i in tqdm(range(self.db_handler.size)):
            news_id = i + 1
            news = self.db_handler.query(id=news_id)[0]
            # build raw text
            text = ' '.join([news.title, news.author, news.publication, news.content])
            # add tokens to index map
            for token, freq in tokenize(text):
                # if a new token comes, create an index chain for it
                if token not in self.idx_map.keys():
                    self.idx_map[token] = list()
                # every element in the index chain should adopt the format of (news id, frequency)
                self.idx_map[token].append((news_id, freq))

    def save(self, path: str):
        with open(path, 'wb') as f:
            pickle.dump(self.idx_map, f)
        self.logger.info(f'saved index map in {path}')

    def load(self, path: str):
        with open(path, 'rb') as f:
            self.idx_map = pickle.load(f)
        self.logger.info(f'loaded index map from {path}')

    @staticmethod
    def _merge(
            news_list_a: list[tuple[int, int]],
            news_list_b: list[tuple[int, int]]
    ) -> list[tuple[int, int]]:

        size_a = len(news_list_a)
        size_b = len(news_list_b)
        ptr_a = 0
        ptr_b = 0
        ret = list()

        while ptr_a < size_a and ptr_b < size_b:
            id_a, freq_a = news_list_a[ptr_a]
            id_b, freq_b = news_list_b[ptr_b]
            if id_a < id_b:
                ret.append((id_a, freq_a))
                ptr_a += 1
            elif id_a > id_b:
                ret.append((id_b, freq_b))
                ptr_b += 1
            else:
                ret.append((id_a, freq_a))
                ret.append((id_b, freq_b))
                ptr_a += 1
                ptr_b += 1

        if ptr_a < size_a:
            ret.extend(news_list_a[ptr_a:])
        if ptr_b < size_b:
            ret.extend(news_list_b[ptr_b:])

        return ret

    @staticmethod
    def _remove_by_id(
            nf_list: list[tuple[int, float]],
            news_id: int
    ):
        def binary_search(
                start_idx: int,
                end_idx: int
        ):
            if start_idx > end_idx:
                return -1
            mid_idx = (start_idx + end_idx) // 2
            mid_id, _ = nf_list[mid_idx]
            if news_id < mid_id:
                return binary_search(start_idx, mid_idx - 1)
            elif news_id > mid_id:
                return binary_search(mid_idx + 1, end_idx)
            else:
                return mid_idx

        idx = binary_search(0, len(nf_list) - 1)
        if idx >= 0:
            del nf_list[idx]

    def match(
            self,
            positive_tokens: list[str],
            negative_tokens: list[str]
    ) -> list[tuple[int, float]]:
        target = list()

        # collect news containing positive tokens
        for token in positive_tokens:
            try:
                target = self._merge(target, self.idx_map[token])
            except KeyError:
                self.logger.debug(f"""couldn't find "{token}" in the token list""")

        # calculate the mean frequency for every item
        recorder = dict()
        for news_id, freq in target:
            if news_id in recorder.keys():
                recorder[news_id] += freq
            else:
                recorder[news_id] = freq
        target = list()
        for news_id, total_freq in recorder.items():
            target.append((news_id, total_freq / len(positive_tokens)))

        # remove news containing negative tokens
        for token in negative_tokens:
            for negative_news_id, _ in self.idx_map[token]:
                self._remove_by_id(target, negative_news_id)

        # sort the result by frequency
        target = sorted(target, key=lambda x: x[1], reverse=True)

        return target
