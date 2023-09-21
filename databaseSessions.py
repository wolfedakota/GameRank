from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Game, Genre


engine = create_engine('sqlite:///database.sql')
Session = sessionmaker(bind=engine)

session = Session()

games = session.query(Game).all()

for game in games:
    if isinstance(game.genre_id, str) and game.genre_id != '':
        genre_id = [int(id_str) for id_str in game.genre_id.split(',')]
    elif game.genre_id == '':
        genre_id = [-1]
    else:
        genre_id = [game.genre_id]

    genres = session.query(Genre).filter(Genre.id.in_(genre_id)).all()

    game.genres.extend(genres)

session.commit()