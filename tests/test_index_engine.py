from pytrieval.index_engine import IndexEngine
from pytrieval.database.handler import Handler
from pytrieval import config

engine = IndexEngine(Handler(config.database.url))
engine.build()
engine.save(config.path.engine_map)
engine.load(config.path.engine_map)
pass
for i in engine.match(
    positive_tokens=['house', 'health'],
    negative_tokens=['police']
):
    print(i)

