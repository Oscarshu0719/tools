# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import math
import os
import re
import requests
from tqdm import tqdm


"""
    Image downloader of https://www.xsnvshen.com/.

    Usage:
        python xsnvshen_image_downloader.py

    Notice:
        `MODEL_NO`, `ALBUM_NO` and `DOWNLOAD_FROM_MODEL` are changeable.
"""

# Change `MODEL_NO` to specify different model.
MODEL_NO = 0
# Change `ALBUM_NO` to specify different album.
ALBUM_NO = 0
"""
DOWNLOAD_FROM_MODEL: 
    True: Download all albums of a model.
    False: Download only one album.
"""
DOWNLOAD_FROM_MODEL = True

URL_ROOT = 'https://www.xsnvshen.com/'
URL_ALBUM = URL_ROOT + 'album/{}/'
URL_MODEL = URL_ROOT + 'girl/{}/'

PATTERN_HREF = '/album/(.*)'

MAX_ALBUMS_ONE_PAGE = 40

INVALID_CHAR = {'\\', '/', ':', '*', '?', '"', '<', '>', '|'}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
}

root_path = '.'

def download_one_album(album_no, directly_download_album=False):
    # Explore image urls.
    html = requests.get(URL_ALBUM.format(album_no), verify=False).text
    soup = BeautifulSoup(html, 'lxml')
    img_src = 'https:' + soup.select(".origin_image.lazy")[0]["data-original"]
    img_src = img_src[: img_src.rfind("/") + 1] + '{:03d}.jpg'
    img_num = len(soup.select(".swl-item"))
    album_name = soup.select("title")[0].text
    album_name = album_name[: album_name.rfind("_")]

    # Download images.
    path = os.path.join(root_path, album_name)
    if not os.path.exists(path): 
        os.makedirs(path)
    elif directly_download_album:
        print('\n* Error: The output folder exists. Exit this program.')
        return

    if directly_download_album:
        print('\n* Info: Start downloading images (album_name: {}).'.format(album_name))
    
    for i in range(img_num):
        save_path = os.path.join(path, '{}.jpg'.format(i))
        headers['Referer'] = 'https://www.xsnvshen.com/album/{}'.format(album_no)
        img = requests.get(img_src.format(i), headers=headers)

        with open(save_path, 'wb') as img_file:
            img_file.write(img.content)

def download_albums(model_no):
    html = requests.get(URL_MODEL.format(str(model_no)), verify=False).text
    soup = BeautifulSoup(html, 'lxml')
    model_name = soup.select('.bas-cont')[0].text
    albums = soup.select(".star-mod-bd a")
    album_list = list()
    for album in albums:
        match = re.search(PATTERN_HREF, album["href"])
        if match:
            album_list.append(match.group(1))

    global root_path
    root_path = os.path.join('.', model_name)
    if not os.path.exists(root_path): 
        os.makedirs(root_path)
    else:
        print('\n* Error: The output folder exists. Exit this program.')
        return 
    
    print('\n* Info: Finish exploring {} albums (model_name: {}).\n'.format(len(album_list), model_name))

    pbar = tqdm(total=len(album_list))
    pbar.set_description("Progress")

    for album_no in album_list:
        download_one_album(album_no)

        pbar.update(1)


if __name__ == '__main__':
    if DOWNLOAD_FROM_MODEL:
        download_albums(MODEL_NO)
    else:
        download_one_album(ALBUM_NO, True)
