from time import sleep

import requests as requests
from bs4 import BeautifulSoup as bs
import re, os

from sql import PostUrl, commit

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}

url = 'https://pikabu.ru/best'
url_list = ['https://pikabu.ru/best', 'https://pikabu.ru/', 'https://pikabu.ru/new']


def parse_posts_urls(url):
    session = requests.Session()
    request = session.get(url, headers=headers)
    if request.status_code == 200:
        print('Get page = ', url)
        soup = bs(request.content, 'html.parser')
        posts_list = soup.find_all('a', 'story__title-link', 'story__title-link_visited')
        for post in posts_list:
            url = post['href']
            title_name = post.text
            id = get_id_url(url)
            category = soup.title.text
            post = PostUrl(title=title_name, pika_id=id, url=url, category=category)
        print('parse complete = ', url)
    else:
        print("Page not exist")


def get_id_url(url):
    result = re.findall(r'_(\d+)$', url)[0]
    return result


if __name__ == '__main__':
    for url in url_list:
        sleep(1)
        parse_posts_urls(url)
        commit()
