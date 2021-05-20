from collections import Counter

from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords


def lemmatize(word: str) -> str:
    lemma = WordNetLemmatizer()
    word = lemma.lemmatize(word, 'v')
    word = lemma.lemmatize(word, 'n')
    return word


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
