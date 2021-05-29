from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pytrieval.database.models import Base, News
from pytrieval.logger import Logger


class Handler:
    def __init__(self, url: str):
        engine = create_engine(url)
        self.logger = Logger(self.__class__.__name__)
        self._Session = sessionmaker(engine)
        Base.metadata.create_all(engine)

        session = self._Session()
        self.size = session.query(News).count()

        self.logger.debug(f'initialized with url: {url}')

    def insert(self, data: News):
        session = self._Session()
        session.add(data)
        session.commit()
        self.logger.debug(f'new data inserted: {data}')
        session.close()
        self.size += 1

    def query(self, **kwargs) -> list[News]:
        self.logger.debug(f'querying parameters: {kwargs}')
        session = self._Session()
        ret = list()
        for i in session.query(News).filter_by(**kwargs):
            ret.append(i)
        session.expunge_all()
        session.close()
        self.logger.debug(f'{len(ret)} items found')
        return ret
