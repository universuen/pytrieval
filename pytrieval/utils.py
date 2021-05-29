from collections import Counter
from typing import Union
from math import log

from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords

from pytrieval.config import path


def lemmatize(word: str) -> str:
    try:
        lemma = WordNetLemmatizer()
        word = lemma.lemmatize(word, 'v')
        word = lemma.lemmatize(word, 'n')
        return word
    except LookupError:
        import nltk
        nltk.download('wordnet')


def tokenize(text: str) -> list[tuple[str, int]]:
    try:
        tokens = word_tokenize(text)
        # remove punctuations
        tokens = [word for word in tokens if word.isalpha()]
        # lower words
        tokens = [word.lower() for word in tokens]
        # remove stop words
        tokens = [word for word in tokens if word not in stopwords.words('english')]
        # lemmatize words
        tokens = [lemmatize(word) for word in tokens]
        return Counter(tokens).most_common()
    except LookupError:
        import nltk
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        return tokenize(text)


def get_text_size(text: str) -> int:
    return len(text.split(' '))


def get_tfidf(
        word_num: int,  # the number of the particular word in the text
        total_word_num: int,  # the number of words in the text
        text_num: int,  # the number of texts containing the particular
        total_text_num: int  # the number of all texts
):
    tf = word_num / total_word_num
    idf = log(total_text_num / (1 + text_num))
    return tf * idf


def tuple_list2dict(list_: list[tuple[int, Union[int, float]]]) -> dict[int, Union[int, float]]:
    ret = dict()
    for i, j in list_:
        ret[i] = j
    return ret
