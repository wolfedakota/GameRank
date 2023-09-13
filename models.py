from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

game_genre_association = Table(
    'game_genre_association',
    Base.metadata,
    Column('game_id', Integer, ForeignKey('games.id')),
    Column('genre_id', String, ForeignKey('genre.id'))
)

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    game_title = Column(String(255))
    game_bio = Column(String(9999))
    game_image = Column(String(255))
    metascore = Column(Integer)
    user_score = Column(Integer)
    gamerank_score = Column(Integer)

    platform_id = Column(Integer, ForeignKey('platform.id'))
    platform = relationship('Platform')

    # genre_id = Column(String(255)) #genre is a string of genre ids, as each games has multiple genres
    genres = relationship('Genre', secondary=game_genre_association)

    release_date = Column(String(255))

    decade_id = Column(Integer, ForeignKey('decade.id'))
    decade = relationship('Decade')


class Platform(Base):
    __tablename__ = 'platform'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

class Genre(Base):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

class Decade(Base):
    __tablename__ = 'decade'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))