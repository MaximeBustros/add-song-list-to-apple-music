from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import time 

import urllib.parse

def get_chrome_options():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    return chrome_options


def launch_chrome_with_options(options):
    #Change chrome driver path accordingly
    chrome_driver = "C:\chromedriver.exe"
    return webdriver.Chrome(chrome_driver, chrome_options=options)


def get_url(term):
    return f"https://music.apple.com/fr/search?term={term}"


def add_songs_to_apple_music(driver, song_list_file, error_file):
    for line in song_list_file.readlines():
        add_song_to_apple_music(driver, line, error_file)

def write_to_file_missing_song(line, error_file):
    error_file.write(f"{line}\n")


def add_song_to_apple_music(driver, song_name, error_file):
    print(f"adding song {song_name} to apple music")
    try:
        # Urlify term from song_name
        term = urllib.parse.quote(song_name)

        # Get url to query
        url = get_url(term)

        # Query url
        driver.get(url)

        # Get song section
        first_song_section = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.section[aria-label="Morceaux"] div.cloud-buttons[data-testid="cloud-buttons"]'))
        )


        ActionChains(driver).move_to_element(first_song_section).pause(1).perform()

        # Find add library button
        add_to_library_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.section[aria-label="Morceaux"] div.add-to-library-button[data-testid="add-to-library-button"]'))
        )

        # Add song
        ActionChains(driver).click(add_to_library_button).pause(1).perform()
    except Exception as e:
        print(e.with_traceback)
        write_to_file_missing_song(song_name, error_file)
    else:
        print(f"successfully added song {song_name} to apple music")


def run():
    # Launch chrome
    chrome_options = get_chrome_options()
    driver = launch_chrome_with_options(chrome_options)

    # Open file and loop over lines to add songs
    try:
        song_list_file = open('text.md', 'r', encoding="utf-8")
        error_file = open("missing_songs.txt", "w", encoding="utf-8")

        # Add each song to apple music
        add_songs_to_apple_music(driver, song_list_file, error_file)
    finally:
        song_list_file.close()
        error_file.close()


if __name__ == "__main__":
    run()