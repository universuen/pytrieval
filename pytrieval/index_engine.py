"""
Definition of IndexEngine
"""
import pickle
from typing import Union

from tqdm import tqdm

from pytrieval.database.handler import Handler
from pytrieval.logger import Logger
from pytrieval.utils import tokenize, get_text_size, get_tfidf


class IndexEngine:

    def __init__(self, db_handler: Handler):
        self.db_handler = db_handler
        self.db_handler.logger.disabled = True
        self.size = self.db_handler.size
        self.logger = Logger(self.__class__.__name__)
        self.idx_map = dict()

    def build_freq_engine(self):
        self.idx_map = dict()
        self.logger.info('building index engine in "freq" mode')
        # load all news from the database
        for i in tqdm(range(self.size)):
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

    def build_tfidf_engine(self):
        self.logger.info('building index engine in "TFIDF" mode')
        # firstly, build a freq map
        self.logger.disabled = True
        self.build_freq_engine()
        self.logger.disabled = False
        # then calculate every item's TF-IDF in the map
        total_num = self.size
        self.logger.info('calculating TF-IDF for each word')
        for word in tqdm(self.idx_map.keys()):
            text_num = len(self.idx_map[word])
            for idx, (news_id, freq) in enumerate(self.idx_map[word]):
                word_num = freq
                news = self.db_handler.query(id=news_id)[0]
                text = ' '.join([news.title, news.author, news.publication, news.content])
                text_size = get_text_size(text)
                self.idx_map[word][idx] = (news_id, get_tfidf(word_num, text_size, text_num, total_num))

    def save(self, path: str):
        with open(path, 'wb') as f:
            pickle.dump(self.idx_map, f)
        self.logger.info(f'saved index map in {path}')

    def load(self, path: str):
        with open(path, 'rb') as f:
            self.idx_map = pickle.load(f)
        self.logger.info(f'loaded index map from {path}')

    def get(self, token: str) -> list[tuple[int, Union[int, float]]]:
        try:
            return self.idx_map[token]
        except KeyError:
            return []
