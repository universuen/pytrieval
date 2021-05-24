"""
Definition of IndexEngine
"""
import pickle
from typing import Union

from tqdm import tqdm

from src.database.handler import Handler
from src.logger import Logger
from src.utils import tokenize


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

    def get(self, token: str) -> list[tuple[int, Union[int, float]]]:
        try:
            return self.idx_map[token]
        except KeyError:
            return []

