import requests as requests
from bs4 import BeautifulSoup as bs
import re, os

posts_folder = 'posts'
debug = True

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}

target_url = 'https://pikabu.ru/story/vozvrat_tovara_v_sportmaster_7155894'


def parse_post(post_url, headers):
    post = {}
    post['content'] = []
    post['images'] = {}
    post['url'] = post_url
    post['tags'] = []
    session = requests.Session()
    request = session.get(post_url, headers=headers)
    if request.status_code == 200:
        print('Connect to post page')
        soup = bs(request.content, 'html.parser')

        post['name'] = str(soup.find('span', 'story__title-link').text).strip()

        post['author'] = str(soup.find_all('a', 'user__nick')[0].text).strip()

        post['time'] = str(soup.find_all('time', 'caption', 'story__datetime')[0]['datetime']).strip()

        post_content = soup.find_all('div', 'story-block')
        for block in post_content:
            if block.text:
                text = str(block.text).strip()
                if text:
                    post['content'].append(text)

            if block.img:
                img_link = str(block.img['data-large-image']).strip()
                post['content'].append(get_image_name(img_link))

        tags = soup.find_all('a', 'tags__tag', 'data-tag-menu')
        for tag in tags:
            tag_text = str(tag.text).strip()
            post['tags'].append(tag_text)

    else:
        print('connection error')

    print(post['tags'])
    return post


def get_post_id(url):
    result = re.findall(r'_(\d+)', url)[0]
    return result


def get_image_name(url):
    return str(re.findall(r'/(\d+\.\w+)', url)[0])


def create_post_folder(post_id):
    post_folder = os.path.join(posts_folder, post_id)
    if not os.path.exists(posts_folder):
        os.mkdir(posts_folder)
    if not os.path.exists(post_folder):
        os.mkdir(post_folder)


def download_image(url, post_id='test'):
    create_post_folder(post_id)
    file_full_name = os.path.join(posts_folder, post_id, get_image_name(url))
    session = requests.Session()
    image = session.get(url, headers=headers)
    if not os.path.exists(file_full_name):
        file = open(file_full_name, 'wb')
        file.write(image.content)
        file.close()


if __name__ == '__main__':
    # parse_post(target_url, headers)
    parse_post('https://pikabu.ru/story/v_kazani_snyali_s_vyistavki_chast_kartin_vasi_lozhkina_7159561', headers)
