"""
Definition of Pytrieval
"""
from pytrieval.logger import Logger
from pytrieval.database.handler import Handler
from pytrieval.index_engine import IndexEngine
from pytrieval.query_parser import QueryParser
from pytrieval import config


class Pytrieval:
    def __init__(self):
        self.logger = Logger(self.__class__.__name__)
        self.logger.info('initializing ...')
        self.engine = IndexEngine(Handler(config.database.url))
        self.engine.logger.disabled = True
        self.logger.debug('loading index engine')
        try:
            self.engine.load(config.path.engine_map)
        except Exception as e:
            self.logger.debug(f'failed to load the existing engine due to {e}')
            self.logger.debug('building new engine')
            self.engine.build()
            self.logger.debug('engine was built successfully')
            self.engine.save(config.path.engine_map)
        self.parser = QueryParser()

    def run(self):
        print('welcome!')
        while True:
            query = input('> ')
            positive_tokens, negative_tokens = self.parser.parse(query)
            result = self.engine.match(positive_tokens, negative_tokens)
            for news_id, recommendation_score in result:
                print(f'news_id: {news_id}, recommendation_score: {recommendation_score}')
