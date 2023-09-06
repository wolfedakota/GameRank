from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

#chrome_driver_version = '116.0.5845.110'
#chrome_driver_path = '/root/GamerRank/chromedriver-win64/chromedriver.exe'
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())

url = "https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?view=detailed&sort=desc&page=0"

driver.get(url)
driver.implicitly_wait(10)

main_content = driver.find_element(By.ID, "main_content")

titles = main_content.find_elements(By.CSS_SELECTOR, "a.title")

total_titles = 0

for title in titles:
    if total_titles >= 10:
        break

    h3_element = title.find_element(By.TAG_NAME, "h3")
    game_title = h3_element.text
    print(game_title)

    total_titles += 1

driver.quit()