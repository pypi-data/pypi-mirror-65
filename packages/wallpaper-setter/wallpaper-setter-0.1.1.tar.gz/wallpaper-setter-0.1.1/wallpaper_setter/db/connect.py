from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from wallpaper_setter.db.models import Base

class Database:
    _instance = None
    _engine = None
    _Session = None

    def __new__(self, uri):
        if self._instance is None:
            self._instance = super(Database, self).__new__(self)
            self._engine = create_engine(uri)
            self._Session = sessionmaker(bind=self._engine)
        return self._instance

    def get_engine(self):
        return self._engine

    def get_session(self):
        return self._Session()

    def create_tables(self):
        Base.metadata.create_all(self._engine)
