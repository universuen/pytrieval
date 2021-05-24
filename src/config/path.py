from pathlib import Path

src = Path(__file__).absolute().parent.parent
project = src.parent
data = project / 'data'


freq_engine_map = data / 'freq_engine_map.pkl'
tfidf_engine_map = data / 'tfidf_engine_map.pkl'
