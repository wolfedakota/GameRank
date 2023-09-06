from bs4 import BeautifulSoup
import requests
import math
import sqlite3
import time

# Initial URL
BASE_URL = "https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?view=detailed&sort=desc&page={}"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

connection = sqlite3.connect('database.sql')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY,
    game_title TEXT,
    game_bio TEXT,
    game_image TEXT,
    metascore SMALLINT,
    user_score SMALLINT,
    gamerank_score SMALLINT,
    platform_id SMALLINT,
    genre_id,
    release_date TEXT,
    decade_id SMALLINT,
    developer_id SMALLINT
)
''')
               
cursor.execute('''
CREATE TABLE IF NOT EXISTS platform (
    id INTEGER PRIMARY KEY,
    name TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS genre (
    id INTEGER PRIMARY KEY,
    name TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS developer (
    id INTEGER PRIMARY KEY,
    name TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS decade (
    id INTEGER PRIMARY KEY,
    name TEXT
)
''')
                              
connection.commit()

games_list = []

current_page = 0
existing_platforms = set()
existing_genres = set()
existing_developers = set()
existing_decades = set()

platform_id_mapping = {}
current_platform_id = 0

developer_id_mapping = {}
current_developer_id = 0

genre_id_mapping = {}
current_genre_id = 0

while True:
    URL = BASE_URL.format(current_page)
    page = requests.get(URL, headers=headers, allow_redirects=False)
    page_content = page.content.decode("utf-8")
    response = BeautifulSoup(page.content, "html.parser")
    main_content = response.find(id="main_content")
    game_titles = main_content.find_all("a", class_="title")

    if not game_titles:  # No more pages to scrape
        break

    REQUESTS = 10
    TIME_INTERVAL = 15

    unique_games = {}

    for id, title in enumerate(game_titles):
        game_info = {
            "id": id,
            "genre_ids": [],
            "developer_id": None,
            "developer": "N/A",
            "platform": "N/A",
            "release_date": "N/A",
            "summary": "N/A",
        }

        if id % REQUESTS == 0 and id != 0:
            print(f"Pausing for {TIME_INTERVAL} seconds to comply with rate limiting")
            time.sleep(TIME_INTERVAL)

        h3_element = title.find("h3")
        if h3_element:
            game_info["title"] = h3_element.text.strip()
            print(game_info["title"])

        platform_div = title.find_next("div", class_="platform")
        platform_span = platform_div.find("span", class_="data")
        platform_text = platform_span.text.strip() if platform_span else "N/A"

        if platform_text not in platform_id_mapping:
            platform_id_mapping[platform_text] = current_platform_id
            current_platform_id += 1

        game_info["platform"] = platform_text

        platform_id = platform_id_mapping.get(platform_text)
        game_info["platform_id"] = platform_id

        clamp_details_div = title.find_next("div", class_="clamp-details")
        release_date_spans = clamp_details_div.find_all("span")
        release_date_span = release_date_spans[-1]
        release_date_text = release_date_span.text.strip() if release_date_span else "N/A"
        release_date_year = int(release_date_text[-4:])

        if 1950 <= release_date_year and release_date_year <= 1959:
            decade_id = 0
            decade = "50s"
        elif 1960 <= release_date_year and release_date_year <= 1969:
            decade_id = 1
            decade = "60s"
        elif 1970 <= release_date_year and release_date_year <= 1979:
            decade_id = 2
            decade = "70s"
        elif 1980 <= release_date_year and release_date_year <= 1989:
            decade_id = 3
            decade = "80s"
        elif 1990 <= release_date_year and release_date_year <= 1999:
            decade_id = 4
            decade = "90s"
        elif 2000 <= release_date_year and release_date_year <= 2009:
            decade_id = 5
            decade = "2000s"
        elif 2010 <= release_date_year and release_date_year <= 2019:
            decade_id = 6
            decade = "2010s"
        elif 2020 <= release_date_year and release_date_year <= 2029:
            decade_id = 7
            decade = "2020s"
        else:
            decade_id = 99
            decade = "N/A"

        game_info["release_date"] = release_date_text
        #game_info["release_year"] = release_date_year
        game_info["decade_id"] = decade_id
        game_info["decade"] = decade

        full_game_url = f"https://www.metacritic.com{title['href']}"
        game_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        game_page = requests.get(full_game_url, headers=game_headers, allow_redirects=False)
        game_response = BeautifulSoup(game_page.content, "html.parser")
        #game_info["game_url"] = full_game_url
        game_main_content = game_response.find(id="main_content")

        if game_main_content:

            developer_span = game_main_content.find("span", class_="label", text="Developer:")
            if developer_span:
                developer = developer_span.find_next("a").text.strip()
                game_info["developer"] = developer
            else:
                game_info["developer"] = "N/A"

            if developer not in developer_id_mapping:
                developer_id_mapping[developer] = current_developer_id
                current_developer_id += 1

            developer_id = developer_id_mapping.get(developer)
            game_info["developer_id"] = developer_id if developer_id is not None else None


            genre_li = game_response.find("li", class_="summary_detail product_genre")
            if genre_li:
                genres = {genre.text.strip() for genre in genre_li.find_all("span", class_="data")}
                game_info["genres"] = genres
                genre_ids = []

                for genre in genres:
                    if genre not in genre_id_mapping:
                        genre_id_mapping[genre] = current_genre_id
                        current_genre_id += 1
                    genre_id = genre_id_mapping.get(genre)
                    genre_ids.append(genre_id)

                game_info["genre_ids"] = genre_ids

        else:
            print("Error: game_main_content is None")



        image_wrap_td = title.find_previous("td", class_="clamp-image-wrap")
        image_tag = image_wrap_td.find("img")
        image_src = image_tag["src"]
        game_info["image_src"] = image_src

        summary_div = platform_div.find_next("div", class_="summary")
        summary_text = summary_div.text.strip().replace("\r", "").replace("\n", "")
        game_info["summary"] = summary_text

        metascore_div = summary_div.find_next("div", class_="clamp-metascore")
        metascore_inner_div = metascore_div.find("div", class_=lambda x: "metascore_w" in x)
        metascore_text = int(metascore_inner_div.text) if metascore_inner_div else "N/A"
        game_info["metascore"] = metascore_text

        print(game_info["metascore"])

        userscore_div = metascore_div.find_next("div", class_="clamp-userscore")
        userscore_inner_div = userscore_div.find("div", class_=lambda x: "metascore_w" in x)
        if userscore_inner_div.text == "tbd":
            userscore_text = metascore_text
        else:
            userscore_text = int(float(userscore_inner_div.text) * 10) if userscore_inner_div else "N/A"
        game_info["userscore"] = userscore_text

        gamerank_score = (userscore_text + metascore_text) / 2
        gamerank_score = int(math.ceil(gamerank_score))
        game_info["gamerank_score"] = gamerank_score

        #print(game_info["gamerank_score"])

        games_list.append(game_info)

        genre_ids_str = ','.join(map(str, game_info["genre_ids"]))

        game_key = (game_info["title"], game_info["platform_id"])
        if game_key not in unique_games:
            # Add the game to the dictionary and insert it into the database
            unique_games[game_key] = True  # Store it in the dictionary
            cursor.execute('''
                INSERT INTO games (game_title, game_bio, game_image, metascore, user_score, gamerank_score, platform_id, genre_id, release_date, decade_id, developer_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                game_info["title"], game_info["summary"], game_info["image_src"],
                game_info["metascore"], game_info["userscore"], game_info["gamerank_score"],
                game_info["platform_id"], genre_ids_str, game_info["release_date"],
                game_info["decade_id"], game_info["developer_id"]
            ))
            connection.commit()

        cursor.execute('''
            INSERT OR IGNORE INTO platform (id, name)
            VALUES (?, ?)
        ''', (
            game_info["platform_id"], game_info["platform"]))
        connection.commit()

        for genre_id, genre in zip(genre_ids, genres):
            cursor.execute('''
                INSERT OR IGNORE INTO genre (id, name)
                VALUES (?, ?)
            ''', (
                genre_id, genre))
            connection.commit()

        cursor.execute('''
            INSERT OR IGNORE INTO developer (id, name)
            VALUES (?, ?)
        ''', (
            game_info["developer_id"], game_info["developer"]))
        connection.commit()

        cursor.execute('''
            INSERT OR IGNORE INTO decade (id, name)
            VALUES (?, ?)
        ''', (
            game_info["decade_id"], game_info["decade"]))
        connection.commit()

    current_page += 1
    print(f"current page: {current_page}")

print(games_list)
connection.close()