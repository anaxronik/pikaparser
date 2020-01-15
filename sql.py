import datetime

import sqlalchemy
from sqlalchemy import Column, Integer, String, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

print('Версия SQLAlchemy =', sqlalchemy.__version__)

engine = create_engine('sqlite:///DB.sqlite')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class ItemDB:
    id = Column(Integer, primary_key=True)

    def add_to_session(self):
        session.add(self)


class Post(Base, ItemDB):
    __tablename__ = 'posts'
    date_parse = Column(DateTime, default=datetime.datetime.utcnow)
    name = Column(String)
    url = Column(String)
    site_id = Column(String)
    author = Column(String)
    date_create = Column(String)
    text = Column(String)
    tags = Column(String)

    def __init__(self, name=None, url=None, author=None, site_id=None, date_create=None, text=None, tags=None):
        self.name = name
        self.author = author
        self.date_create = date_create
        self.text = text
        self.tags = tags
        self.site_id = site_id
        self.url = url

        self.add_to_session()

    def __repr__(self):
        return f'<Post: name = {self.name}, >'


class PostUrl(Base, ItemDB):
    __tablename__ = 'post_list'
    url = Column(String, unique=True)
    title = Column(String)
    pika_id = Column(String, unique=True)
    date_parse = Column(DateTime, default=datetime.datetime.utcnow)
    category = Column(String)

    def __init__(self, title, pika_id, url, category):
        self.title = title
        self.pika_id = pika_id
        self.url = url
        self.category = category

        self.add_to_session()


def commit():
    session.commit()


def create_tables():
    # Создание таблицы
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_tables()

    for i in range(10):
        post = Post(site_id=i*i+i)
    commit()
