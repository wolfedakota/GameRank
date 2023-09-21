from sqlalchemy.orm import Session
from models import Game, Genre

session = Session()

games = session.query(Game).all()

for game in games:
    genre_ids = game.genre_ids.split(',')  # Assuming genre_ids is a string like "0,1,2"

    genres = session.query(Genre).filter(Genre.id.in_(genre_ids)).all()

    game.genres.extend(genres)

session.commit()