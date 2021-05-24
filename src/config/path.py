from pathlib import Path

src = Path(__file__).absolute().parent.parent
project = src.parent
data = project / 'data'


engine_map = data / 'engine_map.pkl'
