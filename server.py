"""GamerRank Web Application"""

from jinja2 import StrictUndefined
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, flash, redirect, session
from databaseSessions import Session
from models import Game, Platform, Genre, Decade
from sqlalchemy import and_, or_, desc, asc

app = Flask(__name__)

@app.route('/')
def index():
    """Homepage"""
    session = Session()

    top_games = session.query(Game) \
        .filter(Game.release_date.like('%2023%')) \
        .group_by(Game.game_title) \
        .order_by(desc(Game.gamerank_score)) \
        .limit(3) \
        .all()

    bottom_games = session.query(Game) \
        .filter(Game.release_date.like('%2023%')) \
        .group_by(Game.game_title) \
        .order_by(asc(Game.gamerank_score)) \
        .limit(3) \
        .all()
    
    session.close()

    # Pass the data to the HTML template
    return render_template('homepage.html', top_games=top_games, bottom_games=bottom_games)

@app.route('/PopularFranchises')
def popular_franchises():
    """A page containing a list of the top gaming franchises"""

    return render_template("popularFranchises.html")

@app.route('/BestGames')
def best_games():
    """A page containing a list of the top games"""

    return render_template("topGames.html")

@app.route('/WorstGames')
def worst_games():
    """A page containing a list of the worst games"""

    return render_template("worstGames.html")

@app.route('/ComparisonTool')
def comparison_tool():
    """A page containing a tool for comparing games"""

    return render_template("comparisonTool.html")

@app.route('/Profile')
def profile():
    """A page containing the user's profile"""

    return render_template("profile.html")

@app.route('/FavoriteGames')
def favorite_games():
    """A page containing a list of the user's favorite games"""

    return render_template("favoriteGames.html")

@app.route('/EditProfile')
def edit_profile():
    """A page containing an editing tool for the user's profile"""

    return render_template("editProfile.html")

@app.route('/Login')
def login():
    """A page containing a login window"""

    return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
