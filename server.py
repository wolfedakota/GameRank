"""GamerRank Web Application"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session

app = Flask(__name__)

@app.route('/')
def index():
    """Homepage"""

    return render_template("homepage.html")

@app.route('/PopularFranchises')
def popular_franchises():
    """A page containing a list of the top gaming franchises"""

    return render_template("popularFranchises.html")

@app.route('/TopGames')
def top_games():
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
    """A page containing a list of the top gaming franchises"""

    return render_template("profile.html")

@app.route('/FavoriteGames')
def favorite_games():
    """A page containing a list of the top gaming franchises"""

    return render_template("favoriteGames.html")

@app.route('/EditProfile')
def edit_profile():
    """A page containing a list of the top gaming franchises"""

    return render_template("editProfile.html")

@app.route('/Login')
def login():
    """A page containing a list of the top gaming franchises"""

    return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
