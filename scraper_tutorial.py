from selenium import webdriver
from time import sleep
import re

YOUTUBE_MUSIC_URL = 'https://www.youtube.com/channel/UC-9-kyTW8ZkZNDHQJ6FgpwQ'


def scroll(driver, time, delay):
    for t in range(0, time):
        driver.execute_script('window.scrollTo(0, 99999);')
        sleep(delay)


def watch_id_from_url(url):
    p = re.compile("watch\\?v=(.{11})")
    return p.search(url).group(1)


def scrape_youtube_music(driver):
    driver.get(YOUTUBE_MUSIC_URL)
    scroll(driver, 5, 1)
    music_list_links = [elem.get_attribute('href') for elem in driver.find_elements_by_xpath('//*[@id="image-container"]/a')]

    for link in music_list_links:
        driver.get(link)
        scroll(driver, 5, 1)

        for thumb_elem in driver.find_elements_by_xpath('//*[@id="thumbnail"]/a'):
            watch_url = thumb_elem.get_attribute('href')
            print(f'watch_id is {watch_id_from_url(watch_url)}')


if __name__ == '__main__':

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('disable-gpu')
    options.add_argument('window-size=1920x1080')
    options.add_argument(
        'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gcko)'
        ' Chrome/61.0.3163.100 Safari/537.36')

    from platform import system

    driver = webdriver.Chrome(f'./driver/{system()}/chromedriver', options=options)
    driver.implicitly_wait(3)

    try:
        print("start")
        scrape_youtube_music(driver)
        print("end")
    finally:
        driver.quit()