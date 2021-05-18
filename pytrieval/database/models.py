from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.dialects.sqlite import INTEGER, TEXT, DATE


Base = declarative_base()


class News(Base):
    __tablename__ = 'news'

    id = Column(INTEGER, primary_key=True)
    title = Column(TEXT)
    publication = Column(TEXT)
    author = Column(TEXT)
    date = Column(DATE)
    url = Column(TEXT)
    content = Column(TEXT)

    def __repr__(self):
        return f'News(id={self.id}, title={self.title})'
