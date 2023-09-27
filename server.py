"""GamerRank Web Application"""

from jinja2 import StrictUndefined
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, flash, redirect, session, url_for, jsonify
from databaseSessions import Session
from models import Game, Platform, Genre, Decade, User, users_favorite_games
from sqlalchemy import and_, or_, desc, asc

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

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

    return render_template('homepage.html', top_games=top_games, bottom_games=bottom_games)

@app.route('/SearchResults', methods=['GET', 'POST'])
def search_results():
    """Search results based on user input from search bar"""
    if request.method == 'POST':
        user_search_result = request.form.get('navSearchBar')

        session = Session()

        allGames = session.query(Game) \
        .order_by(desc(Game.gamerank_score)) \
        .all()

        search_result_games = session.query(Game) \
            .filter(Game.game_title.like(f'%{user_search_result}%')) \
            .order_by(desc(Game.gamerank_score)) \
            .all()
        
        for i, game in enumerate(allGames, start=1):
            game.gamerank = i
        
    return render_template('search_results.html', search_result_games=search_result_games, user_search_result=user_search_result)


@app.route('/PopularFranchises')
def popular_franchises():
    """A page containing data regarding the top gaming franchises"""

    return render_template("popularFranchises.html")

@app.route('/CallOfDuty')
def popular_franchises_COD():
    """A page containing data regarding the COD franchise"""
    session = Session()

    allGames = session.query(Game) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    COD_games = session.query(Game) \
    .filter(Game.game_title.like('%Call of Duty%')) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    for i, game in enumerate(allGames, start=1):
        game.gamerank = i

    return render_template("popularFranchisesCOD.html", COD_games=COD_games)

@app.route('/TheElderScrolls')
def popular_franchises_TES():
    """A page containing data regarding TES franchise"""
    session = Session()

    allGames = session.query(Game) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    TES_games = session.query(Game) \
    .filter(Game.game_title.like('%The Elder Scrolls%')) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    for i, game in enumerate(allGames, start=1):
        game.gamerank = i

    return render_template("popularFranchisesTES.html", TES_games=TES_games)

@app.route('/Fallout')
def popular_franchises_Fallout():
    """A page containing data regarding the Fallout franchise"""
    session = Session()

    allGames = session.query(Game) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    fallout_games = session.query(Game) \
    .filter(Game.game_title.like('%Fallout%')) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    for i, game in enumerate(allGames, start=1):
        game.gamerank = i

    return render_template("popularFranchisesFallout.html", fallout_games=fallout_games)

@app.route('/Halo')
def popular_franchises_Halo():
    """A page containing data regarding the Halo franchise"""
    session = Session()

    allGames = session.query(Game) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    halo_games = session.query(Game) \
    .filter(Game.game_title.like('%Halo%')) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    for i, game in enumerate(allGames, start=1):
        game.gamerank = i

    return render_template("popularFranchisesHalo.html", halo_games=halo_games)

@app.route('/TheLegendOfZelda')
def popular_franchises_Zelda():
    """A page containing data regarding TLOZ franchise"""
    session = Session()

    allGames = session.query(Game) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    TLOZ_games = session.query(Game) \
    .filter(Game.game_title.like('%Zelda%')) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    for i, game in enumerate(allGames, start=1):
        game.gamerank = i

    return render_template("popularFranchisesTLOZ.html", TLOZ_games=TLOZ_games)

@app.route('/Mario')
def popular_franchises_mario():
    """A page containing data regarding Mario franchise"""
    session = Session()

    allGames = session.query(Game) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    mario_games = session.query(Game) \
    .filter(Game.game_title.like('%Mario%')) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    for i, game in enumerate(allGames, start=1):
        game.gamerank = i

    return render_template("popularFranchisesMario.html", mario_games=mario_games)

@app.route('/PopularPlatforms')
def popular_platforms():
    "A page containing data specific to a popular platform"

    return render_template("popularPlatforms.html")

@app.route('/3DS')
def popular_platforms_3DS():
    "A page containing all of the 3DS game data"
    session = Session()

    allGames = session.query(Game) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    threeDS_games = session.query(Game) \
    .order_by(desc(Game.gamerank_score)) \
    .join(Platform) \
    .filter(Platform.name == '3DS') \
    .all()

    gamePlatforms = session.query(Platform) \
    .all()
    
    gameGenres = session.query(Genre) \
    .group_by(Genre.name) \
    .all()

    for i, game in enumerate(allGames, start=1):
        game.gamerank = i

    return render_template("popularPlatforms3DS.html", threeDS_games=threeDS_games, gamePlatforms=gamePlatforms, gameGenres=gameGenres)

@app.route('/DS')
def popular_platforms_DS():
    "A page containing all of the DS game data"
    session = Session()

    allGames = session.query(Game) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    DS_games = session.query(Game) \
    .join(Platform) \
    .filter(Platform.name == 'DS') \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    gamePlatforms = session.query(Platform) \
    .all()
    
    gameGenres = session.query(Genre) \
    .group_by(Genre.name) \
    .all()

    for i, game in enumerate(allGames, start=1):
        game.gamerank = i

    return render_template("popularPlatformsDS.html", DS_games=DS_games, gamePlatforms=gamePlatforms, gameGenres=gameGenres)

@app.route('/Dreamcast')
def popular_platforms_dreamcast():
    "A page containing all of the Dreamcast game data"
    session = Session()

    allGames = session.query(Game) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    dreamcast_games = session.query(Game) \
    .join(Platform) \
    .filter(Platform.name == 'Dreamcast') \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    gamePlatforms = session.query(Platform) \
    .all()
    
    gameGenres = session.query(Genre) \
    .group_by(Genre.name) \
    .all()

    for i, game in enumerate(allGames, start=1):
        game.gamerank = i

    return render_template("popularPlatformsDreamcast.html", dreamcast_games=dreamcast_games, gamePlatforms=gamePlatforms, gameGenres=gameGenres)

@app.route('/GBA')
def popular_platforms_GBA():
    "A page containing all of the GBA game data"
    session = Session()

    allGames = session.query(Game) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    GBA_games = session.query(Game) \
    .join(Platform) \
    .filter(Platform.name == 'Game Boy Advance') \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    gamePlatforms = session.query(Platform) \
    .all()
    
    gameGenres = session.query(Genre) \
    .group_by(Genre.name) \
    .all()

    for i, game in enumerate(allGames, start=1):
        game.gamerank = i

    return render_template("popularPlatformsGBA.html", GBA_games=GBA_games, gamePlatforms=gamePlatforms, gameGenres=gameGenres)

@app.route('/GameCube')
def popular_platforms_GameCube():
    "A page containing all of the GBA game data"
    session = Session()

    allGames = session.query(Game) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    GameCube_games = session.query(Game) \
    .join(Platform) \
    .filter(Platform.name == 'GameCube') \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    gamePlatforms = session.query(Platform) \
    .all()
    
    gameGenres = session.query(Genre) \
    .group_by(Genre.name) \
    .all()

    for i, game in enumerate(allGames, start=1):
        game.gamerank = i

    return render_template("popularPlatformsGameCube.html", GameCube_games=GameCube_games, gamePlatforms=gamePlatforms, gameGenres=gameGenres)

@app.route('/N64')
def popular_platforms_N64():
    "A page containing all of the N64 game data"
    session = Session()

    allGames = session.query(Game) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    N64_games = session.query(Game) \
    .join(Platform) \
    .filter(Platform.name == 'Nintendo 64') \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    gamePlatforms = session.query(Platform) \
    .all()
    
    gameGenres = session.query(Genre) \
    .group_by(Genre.name) \
    .all()

    for i, game in enumerate(allGames, start=1):
        game.gamerank = i

    return render_template("popularPlatformsN64.html", N64_games=N64_games, gamePlatforms=gamePlatforms, gameGenres=gameGenres)

@app.route('/PC')
def popular_platforms_PC():
    "A page containing all of the PC game data"
    session = Session()

    allGames = session.query(Game) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    PC_games = session.query(Game) \
    .join(Platform) \
    .filter(Platform.name == 'PC') \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    gamePlatforms = session.query(Platform) \
    .all()
    
    gameGenres = session.query(Genre) \
    .group_by(Genre.name) \
    .all()

    for i, game in enumerate(allGames, start=1):
        game.gamerank = i

    return render_template("popularPlatformsPC.html", PC_games=PC_games, gamePlatforms=gamePlatforms, gameGenres=gameGenres)

@app.route('/PSP')
def popular_platforms_PSP():
    "A page containing all of the PSP game data"
    session = Session()

    allGames = session.query(Game) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    PSP_games = session.query(Game) \
    .join(Platform) \
    .filter(Platform.name == 'PSP') \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    gamePlatforms = session.query(Platform) \
    .all()
    
    gameGenres = session.query(Genre) \
    .group_by(Genre.name) \
    .all()

    for i, game in enumerate(allGames, start=1):
        game.gamerank = i

    return render_template("popularPlatformsPSP.html", PSP_games=PSP_games, gamePlatforms=gamePlatforms, gameGenres=gameGenres)

@app.route('/PS1')
def popular_platforms_PS1():
    "A page containing all of the PS1 game data"
    session = Session()

    allGames = session.query(Game) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    PS1_games = session.query(Game) \
    .join(Platform) \
    .filter(Platform.name == 'PlayStation') \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    gamePlatforms = session.query(Platform) \
    .all()
    
    gameGenres = session.query(Genre) \
    .group_by(Genre.name) \
    .all()

    for i, game in enumerate(allGames, start=1):
        game.gamerank = i

    return render_template("popularPlatformsPS1.html", PS1_games=PS1_games, gamePlatforms=gamePlatforms, gameGenres=gameGenres)

@app.route('/PS2')
def popular_platforms_PS2():
    "A page containing all of the PS2 game data"
    session = Session()

    allGames = session.query(Game) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    PS2_games = session.query(Game) \
    .join(Platform) \
    .filter(Platform.name == 'PlayStation 2') \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    gamePlatforms = session.query(Platform) \
    .all()
    
    gameGenres = session.query(Genre) \
    .group_by(Genre.name) \
    .all()

    for i, game in enumerate(allGames, start=1):
        game.gamerank = i

    return render_template("popularPlatformsPS2.html", PS2_games=PS2_games, gamePlatforms=gamePlatforms, gameGenres=gameGenres)

@app.route('/PS3')
def popular_platforms_PS3():
    "A page containing all of the PS3 game data"
    session = Session()

    allGames = session.query(Game) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    PS3_games = session.query(Game) \
    .join(Platform) \
    .filter(Platform.name == 'PlayStation 3') \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    gamePlatforms = session.query(Platform) \
    .all()
    
    gameGenres = session.query(Genre) \
    .group_by(Genre.name) \
    .all()

    for i, game in enumerate(allGames, start=1):
        game.gamerank = i

    return render_template("popularPlatformsPS3.html", PS3_games=PS3_games, gamePlatforms=gamePlatforms, gameGenres=gameGenres)

@app.route('/PS4')
def popular_platforms_PS4():
    "A page containing all of the PS4 game data"
    session = Session()

    allGames = session.query(Game) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    PS4_games = session.query(Game) \
    .join(Platform) \
    .filter(Platform.name == 'PlayStation 4') \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    gamePlatforms = session.query(Platform) \
    .all()
    
    gameGenres = session.query(Genre) \
    .group_by(Genre.name) \
    .all()

    for i, game in enumerate(allGames, start=1):
        game.gamerank = i

    return render_template("popularPlatformsPS4.html", PS4_games=PS4_games, gamePlatforms=gamePlatforms, gameGenres=gameGenres)

@app.route('/PS5')
def popular_platforms_PS5():
    "A page containing all of the PS5 game data"
    session = Session()

    allGames = session.query(Game) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    PS5_games = session.query(Game) \
    .join(Platform) \
    .filter(Platform.name == 'PlayStation 5') \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    gamePlatforms = session.query(Platform) \
    .all()
    
    gameGenres = session.query(Genre) \
    .group_by(Genre.name) \
    .all()

    for i, game in enumerate(allGames, start=1):
        game.gamerank = i

    return render_template("popularPlatformsPS5.html", PS5_games=PS5_games, gamePlatforms=gamePlatforms, gameGenres=gameGenres)

@app.route('/PSVita')
def popular_platforms_PSVita():
    "A page containing all of the PS Vita game data"
    session = Session()

    allGames = session.query(Game) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    PSVita_games = session.query(Game) \
    .join(Platform) \
    .filter(Platform.name == 'PlayStation Vita') \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    gamePlatforms = session.query(Platform) \
    .all()
    
    gameGenres = session.query(Genre) \
    .group_by(Genre.name) \
    .all()

    for i, game in enumerate(allGames, start=1):
        game.gamerank = i

    return render_template("popularPlatformsPSVita.html", PSVita_games=PSVita_games, gamePlatforms=gamePlatforms, gameGenres=gameGenres)

@app.route('/Stadia')
def popular_platforms_Stadia():
    "A page containing all of the Stadia game data"
    session = Session()

    allGames = session.query(Game) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    stadia_games = session.query(Game) \
    .join(Platform) \
    .filter(Platform.name == 'Stadia') \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    gamePlatforms = session.query(Platform) \
    .all()
    
    gameGenres = session.query(Genre) \
    .group_by(Genre.name) \
    .all()

    for i, game in enumerate(allGames, start=1):
        game.gamerank = i

    return render_template("popularPlatformsStadia.html", stadia_games=stadia_games, gamePlatforms=gamePlatforms, gameGenres=gameGenres)

@app.route('/Switch')
def popular_platforms_Switch():
    "A page containing all of the Switch game data"
    session = Session()

    allGames = session.query(Game) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    switch_games = session.query(Game) \
    .join(Platform) \
    .filter(Platform.name == 'Switch') \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    gamePlatforms = session.query(Platform) \
    .all()
    
    gameGenres = session.query(Genre) \
    .group_by(Genre.name) \
    .all()

    for i, game in enumerate(allGames, start=1):
        game.gamerank = i

    return render_template("popularPlatformsSwitch.html", switch_games=switch_games, gamePlatforms=gamePlatforms, gameGenres=gameGenres)

@app.route('/Wii')
def popular_platforms_Wii():
    "A page containing all of the Wii game data"
    session = Session()

    allGames = session.query(Game) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    wii_games = session.query(Game) \
    .join(Platform) \
    .filter(Platform.name == 'Wii') \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    gamePlatforms = session.query(Platform) \
    .all()
    
    gameGenres = session.query(Genre) \
    .group_by(Genre.name) \
    .all()

    for i, game in enumerate(allGames, start=1):
        game.gamerank = i

    return render_template("popularPlatformsWii.html", wii_games=wii_games, gamePlatforms=gamePlatforms, gameGenres=gameGenres)

@app.route('/WiiU')
def popular_platforms_WiiU():
    "A page containing all of the Wii U game data"
    session = Session()

    allGames = session.query(Game) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    wiiu_games = session.query(Game) \
    .join(Platform) \
    .filter(Platform.name == 'Wii U') \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    gamePlatforms = session.query(Platform) \
    .all()
    
    gameGenres = session.query(Genre) \
    .group_by(Genre.name) \
    .all()

    for i, game in enumerate(allGames, start=1):
        game.gamerank = i

    return render_template("popularPlatformsWiiU.html", wiiu_games=wiiu_games, gamePlatforms=gamePlatforms, gameGenres=gameGenres)

@app.route('/Xbox')
def popular_platforms_Xbox():
    "A page containing all of the Xbox game data"
    session = Session()

    allGames = session.query(Game) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    xbox_games = session.query(Game) \
    .join(Platform) \
    .filter(Platform.name == 'Xbox') \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    gamePlatforms = session.query(Platform) \
    .all()
    
    gameGenres = session.query(Genre) \
    .group_by(Genre.name) \
    .all()

    for i, game in enumerate(allGames, start=1):
        game.gamerank = i

    return render_template("popularPlatformsXbox.html", xbox_games=xbox_games, gamePlatforms=gamePlatforms, gameGenres=gameGenres)

@app.route('/Xbox360')
def popular_platforms_Xbox360():
    "A page containing all of the Xbox 360 game data"
    session = Session()

    allGames = session.query(Game) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    xbox360_games = session.query(Game) \
    .join(Platform) \
    .filter(Platform.name == 'Xbox 360') \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    gamePlatforms = session.query(Platform) \
    .all()
    
    gameGenres = session.query(Genre) \
    .group_by(Genre.name) \
    .all()

    for i, game in enumerate(allGames, start=1):
        game.gamerank = i

    return render_template("popularPlatformsXbox360.html", xbox360_games=xbox360_games, gamePlatforms=gamePlatforms, gameGenres=gameGenres)

@app.route('/XboxOne')
def popular_platforms_XboxOne():
    "A page containing all of the Xbox One game data"
    session = Session()

    allGames = session.query(Game) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    xboxOne_games = session.query(Game) \
    .join(Platform) \
    .filter(Platform.name == 'Xbox One') \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    gamePlatforms = session.query(Platform) \
    .all()
    
    gameGenres = session.query(Genre) \
    .group_by(Genre.name) \
    .all()

    for i, game in enumerate(allGames, start=1):
        game.gamerank = i

    return render_template("popularPlatformsXboxOne.html", xboxOne_games=xboxOne_games, gamePlatforms=gamePlatforms, gameGenres=gameGenres)

@app.route('/XboxSeriesX')
def popular_platforms_XboxSeriesX():
    "A page containing all of the Xbox Series X game data"
    session = Session()

    allGames = session.query(Game) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    xboxSeriesX_games = session.query(Game) \
    .join(Platform) \
    .filter(Platform.name == 'Xbox Series X') \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    gamePlatforms = session.query(Platform) \
    .all()
    
    gameGenres = session.query(Genre) \
    .group_by(Genre.name) \
    .all()

    for i, game in enumerate(allGames, start=1):
        game.gamerank = i

    return render_template("popularPlatformsXboxSeriesX.html", xboxSeriesX_games=xboxSeriesX_games, gamePlatforms=gamePlatforms, gameGenres=gameGenres)

@app.route('/completeDatabase')
def complete_database():
    "A page containing the entire games table"
    session = Session()

    allGames = session.query(Game) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    gamePlatforms = session.query(Platform) \
    .all()
    
    gameGenres = session.query(Genre) \
    .group_by(Genre.name) \
    .all()

    for i, game in enumerate(allGames, start=1):
        game.gamerank = i

    return render_template("completeDatabase.html", allGames=allGames, gamePlatforms=gamePlatforms, gameGenres=gameGenres)

@app.route('/add_to_favorites', methods=['POST'])
def add_to_favorites():
    """Adds favorites to the user's favorite games"""
    SQLsession = Session()

    game_id = request.form.get('gameId')
    user_id = session.get('user_id')
    if user_id:
        try:
            ins = users_favorite_games.insert().values(user_id=user_id, game_id=game_id)
            SQLsession.execute(ins)
            SQLsession.commit()
            return jsonify({'message': 'Game added to favorites!'})
        except Exception as e:
            # Handle database errors, log the exception, and return an error response
            print(f"Database error: {e}")
            return jsonify({'message': 'Error adding game to favorites.'}), 500
    else:
        return redirect(url_for('login'))

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
    session = Session()

    tableGames = session.query(Game) \
        .order_by(desc(Game.gamerank_score)) \
        .all()
    
    for i, game in enumerate(tableGames, start=1):
        game.gamerank = i
    
    # rightTableGames = session.query(Game) \
    #     .order_by(desc(Game.metascore)) \
    #     .all()

    gamePlatforms = session.query(Platform) \
        .all()
    
    gameGenres = session.query(Genre) \
        .group_by(Genre.name) \
        .all()
    
    gameDecades = session.query(Decade) \
        .all()

    session.close()

    return render_template("comparisonTool.html", tableGames=tableGames, gamePlatforms=gamePlatforms, gameGenres=gameGenres, gameDecades=gameDecades)

@app.route('/Profile')
def profile():
    """A page containing the user's profile"""

    user_id = session.get('user_id')
    if user_id:
        # User is logged in, fetch their information from the database
        SQLsession = Session()
        user = SQLsession.query(User).filter(User.id == user_id).first()
        SQLsession.close()

        return render_template('profile.html', user=user)
    else:
        # User is not logged in, redirect to the login page
        return redirect(url_for('login'))

@app.route('/FavoriteGames')
def favorite_games():
    """A page containing a list of the user's favorite games"""
    SQLsession = Session()

    allGames = SQLsession.query(Game) \
    .order_by(desc(Game.gamerank_score)) \
    .all()

    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))  

    favorite_games = (
        SQLsession.query(Game)
        .join(users_favorite_games)
        .filter(users_favorite_games.c.user_id == user_id)
        .all()
    )

    for i, game in enumerate(allGames, start=1):
        game.gamerank = i

    return render_template('favoriteGames.html', favorite_games=favorite_games)

@app.route('/EditProfile')
def edit_profile():
    """A page containing an editing tool for the user's profile"""

    return render_template("editProfile.html")

@app.route('/Login', methods=['GET', 'POST'])
def login():
    """A page containing a login window"""

    username = request.form.get('username')
    password = request.form.get('password')

    # Query the database to find the user with the given username
    SQLsession = Session()
    user = SQLsession.query(User).filter(User.username == username).first()
    SQLsession.close()

    if user and user.password == password:
        # Valid credentials, store user information in session
        session['user_id'] = user.id
        return redirect(url_for('profile'))
    else:
        valid_credentials = False
        return render_template('login.html', valid_credentials=valid_credentials)
    
@app.route('/LogOut')
def log_out():
    """Log out function"""

    session.clear()

    return redirect('/Login')


@app.route('/newProfile', methods=['GET', 'POST'])
def new_profile():
    """A page containing a profile creation window"""
    if request.method == 'POST':
        new_username = request.form['newUsername']
        new_password = request.form['newPassword']
        new_bio = request.form['newBio']
        new_discord = request.form['newDiscord']
        new_nintendo = request.form['newNintendo']
        new_steam = request.form['newSteam']
        new_playstation = request.form['newPlayStation']
        new_xbox = request.form['newXbox']
        
        # Create a new user instance
        new_user = User(
            username=new_username,
            password=new_password,
            bio=new_bio,
            discord_link=new_discord,
            nintendo_link=new_nintendo,
            steam_link=new_steam,
            playstation_link=new_playstation,
            xbox_link=new_xbox
        )

        # Create a database session
        session = Session()

        try:
            # Add the new user to the session and commit to the database
            session.add(new_user)
            session.commit()
            return redirect("/Login")  # Redirect to a success page
        except Exception as e:
            session.rollback()
            # Handle the error (e.g., display an error message)
        finally:
            session.close()

    return render_template("newProfile.html")

# @app.route('/success')
# def success():
#     return "Account created successfully!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
