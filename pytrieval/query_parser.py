"""
Definition of QueryParser
"""
from pytrieval.utils import lemmatize


class QueryParser:
    def __init__(self):
        pass

    def parse_query(self, query: str) -> tuple[list[str], list[str]]:
        words = query.split()
        positive_tokens = list()
        negative_tokens = list()
        except_ = False
        for i in words:
            if i.isalpha() is False:
                continue
            if i == 'EXCEPT':
                except_ = True
                continue
            if except_:
                negative_tokens.append(self._process(i))
            else:
                positive_tokens.append(self._process(i))
        return positive_tokens, negative_tokens

    @staticmethod
    def _process(word: str):
        return lemmatize(word.lower())
