"""
Definition of QueryParser
"""
from typing import Union

from src.utils import lemmatize
from src.logger import Logger


class MessageParser:
    def __init__(self):
        self.logger = Logger(self.__class__.__name__)

    @staticmethod
    def is_setting(msg: str) -> bool:
        return msg[:3] == 'SET'

    @staticmethod
    def is_selection(msg: str) -> bool:
        return msg[:6] == 'SELECT'

    def parse_setting(self, cmd: str) -> Union[
        tuple[str, Union[str, int]],
        tuple[None, None]
    ]:
        try:
            _, item, value = cmd.split(' ')

            # validity check
            assert item in ('MAX_SIZE', 'MODE')
            if item == 'MAX_SIZE':
                value = int(value)
            else:
                assert value in ('FREQ', 'TFIDF')

            return item.lower(), value

        except Exception as e:
            self.logger.debug(e)
            return None, None

    def parse_selection(self, cmd: str, max_id: int) -> Union[int, None]:
        try:
            _, news_id = cmd.split(' ')
            news_id = int(news_id)

            # validity check
            assert 0 < news_id < max_id

            return news_id

        except Exception as e:
            self.logger.debug(e)
            return None

    def parse_query(self, query: str) -> Union[
        tuple[list[list[str]], list[str]],
        tuple[None, None]
    ]:
        tokens = []
        operators = []
        temp = []

        for i in query.split(' '):
            if i in ['AND', 'OR', 'EXCEPT']:
                operators.append(i)
                tokens.append(temp)
                temp = []
            else:
                temp.append(self._process(i))
        tokens.append(temp)

        return tokens, operators

    @staticmethod
    def _process(word: str):
        return lemmatize(word.lower())


if __name__ == '__main__':
    parser = MessageParser()
    print(parser.parse_query('apple OR banana'))
