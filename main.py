import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import m3u8_To_MP4

options = Options()
options.headless = True
browser = webdriver.Firefox(options=options)
JS_get_network_requests = "var performance = window.performance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;"

url = "https://toonitalia.co/w-i-t-c-h/"
folder = "W-i-t-c-h"

episodes = {}

def get_list_of_episodes(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find('div', class_="entry-content")
    links = results.find_all("a")

    season = None
    episode = 1
    for link in links:

        if (season is not None) and (link.has_attr('href')):
            href = link['href']
            if not href.__contains__('voe.sx'):
                continue
            key = season
            if episode < 9:
                key += 'E0' + str(episode)
            else:
                key += 'E' + str(episode)
            episodes[key] = href

            episode += 1

        if link.has_attr('name'):
            season = link['name']
            episode = 1


def downloader():
    for ep in episodes:
        # ep -> episode number; episodes[ep] -> episode url
        browser.get(episodes[ep])
        network_requests = browser.execute_script(JS_get_network_requests)
        for n in network_requests:
            filename = "{ep}.mp4".format(ep=ep)
            if ".m3u8" in n["name"]:
                m3u8_To_MP4.multithread_download(n["name"], mp4_file_name=filename)

    browser.quit()

if __name__ == '__main__':
    get_list_of_episodes(url)
    downloader()