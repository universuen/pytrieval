from pytrieval.database.handler import Handler
from pytrieval.database.models import News
from pytrieval.config import database

news = News(
    title='test_title',
    content='test_content'
)
print(news)

handler = Handler(database.url)

handler.insert(news)
res = handler.query(title='test_title')
print(res)