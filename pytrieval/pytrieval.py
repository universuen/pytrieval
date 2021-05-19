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
        self.db_handler = Handler(config.database.url)
        self.engine = IndexEngine(self.db_handler)
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
        max_size = -1
        while True:
            msg = input('> ')
            if msg[:3] == 'SET':
                max_size = int(msg.split(' ')[1])
            elif msg[:6] == 'SELECT':
                news_id = int(msg.split(' ')[1])
                news = self.db_handler.query(id=news_id)[0]
                print(f'Title: {news.title}')
                print(f'Author: {news.author}')
                print(f'Publication: {news.publication}')
                content = news.content
                print(f'Content:')
                while len(content) > 0:
                    print(content[:100])
                    content = content[100:]
            else:
                positive_tokens, negative_tokens = self.parser.parse_query(msg)
                result = self.engine.match(positive_tokens, negative_tokens)
                cnt = 0
                for news_id, recommendation_score in result:
                    if cnt != max_size:
                        print(f'{self.db_handler.query(id=news_id)[0]}, recommendation_score: {recommendation_score}')
                    else:
                        break
                    cnt += 1
