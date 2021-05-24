"""
Definition of Pytrieval
"""
from typing import Union

from src.logger import Logger
from src.database.handler import Handler
from src.index_engine import IndexEngine
from src.message_parser import MessageParser
from src.utils import tuple_list2dict
from src import config


class Pytrieval:
    def __init__(self):
        self.logger = Logger(self.__class__.__name__)

        self.logger.info('initializing ...')
        self.db_handler = Handler(config.database.url)
        self.engine = IndexEngine(self.db_handler)
        self.parser = MessageParser()
        self.config = {
            'max_size': 10,
            'mode': 'FREQ'
        }

        self.logger.info('loading index engine')
        self._load_engine()

    def _load_engine(self):
        if self.config['mode'] == 'FREQ':
            try:
                self.engine.load(config.path.freq_engine_map)
            except Exception as e:
                self.logger.info(f'failed to load the existing engine due to {e}')
                self.logger.info('building new engine')
                self.engine.build_freq_engine()
                self.logger.info('engine was built successfully')
                self.engine.save(config.path.freq_engine_map)
        elif self.config['mode'] == 'TFIDF':
            try:
                self.engine.load(config.path.tfidf_engine_map)
            except Exception as e:
                self.logger.info(f'failed to load the existing engine due to {e}')
                self.logger.info('building new engine')
                self.engine.build_tfidf_engine()
                self.logger.info('engine was built successfully')
                self.engine.save(config.path.tfidf_engine_map)

    def run(self):

        print('Welcome!')

        while True:

            msg = input('> ')

            if self.parser.is_setting(msg):
                item, value = self.parser.parse_setting(msg)
                if item is None:
                    print('Wrong setting command. Read README.md for instructions.')
                else:
                    self.config[item] = value
                    if item == 'mode':
                        self._load_engine()

            elif self.parser.is_selection(msg):
                news_id = self.parser.parse_selection(msg, self.db_handler.size)
                if news_id is None:
                    print(f'Wrong selection command. The maximum news ID is {self.db_handler.size}')
                else:
                    self._display_details(news_id)

            else:
                token_lists, operators = self.parser.parse_query(msg)
                news_lists = []
                for token_list in token_lists:
                    news_list = []
                    for token in token_list:
                        if len(news_list) == 0:
                            news_list = self.engine.get(token)
                        else:
                            news_list = self._and_merge(news_list, self.engine.get(token))
                    news_lists.append(news_list)

                operation_switch = {
                    'AND': self._and_merge,
                    'OR': self._or_merge,
                    'EXCEPT': self._except_merge
                }
                current_result = news_lists.pop(0)
                for opt in operators:
                    current_result = operation_switch[opt](current_result, news_lists.pop(0))
                current_result = self._sort_by_score(current_result)
                for i, j in enumerate(current_result):
                    if i == self.config['max_size']:
                        break
                    print(f'\n[{i + 1}]\t\tID: {j[0]}\t\tscore: {j[1]}')
                    self._display_brief(j[0])

    @staticmethod
    def _sort_by_score(news_list: list[tuple[int, Union[int, float]]]):
        return sorted(news_list, key=lambda x: x[1], reverse=True)

    @staticmethod
    def _and_merge(
            news_list_a: list[tuple[int, Union[int, float]]],
            news_list_b: list[tuple[int, Union[int, float]]]
    ) -> list[tuple[int, Union[int, float]]]:
        ret = list()
        dict_a = tuple_list2dict(news_list_a)
        dict_b = tuple_list2dict(news_list_b)
        target_keys = []
        for i in dict_a.keys():
            if i in dict_b.keys():
                target_keys.append(i)
        for i in target_keys:
            ret.append(
                (i, dict_a[i] + dict_b[i])
            )
        return ret

    @staticmethod
    def _or_merge(
            news_list_a: list[tuple[int, Union[int, float]]],
            news_list_b: list[tuple[int, Union[int, float]]]
    ) -> list[tuple[int, Union[int, float]]]:

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
                ret.append((id_a, freq_a + freq_b))
                ptr_a += 1
                ptr_b += 1

        if ptr_a < size_a:
            ret.extend(news_list_a[ptr_a:])
        if ptr_b < size_b:
            ret.extend(news_list_b[ptr_b:])

        return ret

    @staticmethod
    def _except_merge(
            news_list_a: list[tuple[int, Union[int, float]]],
            news_list_b: list[tuple[int, Union[int, float]]]
    ) -> list[tuple[int, Union[int, float]]]:
        ret = list()
        dict_a = tuple_list2dict(news_list_a)
        dict_b = tuple_list2dict(news_list_b)
        target_keys = []
        for i in dict_a.keys():
            if i not in dict_b.keys():
                target_keys.append(i)
        for i in target_keys:
            ret.append(
                (i, dict_a[i])
            )
        return ret

    def _display_brief(self, news_id: int):
        news = self.db_handler.query(id=news_id)[0]
        content = news.content[:197] + '...'
        while len(content) > 0:
            print(content[:100])
            content = content[100:]

    def _display_details(self, news_id: int):
        news = self.db_handler.query(id=news_id)[0]
        print(f'Title: {news.title}')
        print(f'Author: {news.author}')
        print(f'Publication: {news.publication}')
        content = news.content
        print(f'Content:')
        while len(content) > 0:
            print(content[:100])
            content = content[100:]
