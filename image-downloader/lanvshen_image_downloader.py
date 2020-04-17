# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import math
import os
import requests
from tqdm import tqdm


"""
    Image downloader of https://www.lanvshen.com/.

    Usage:
        python lanvshen_image_downloader.py

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
DOWNLOAD_FROM_MODEL = False

URL_ROOT = 'https://www.lanvshen.com/'
URL_ALBUM = URL_ROOT + 'a/{}/'
URL_MODEL = URL_ROOT + 't/{}/'

IMG = 'https://img.hywly.com/a/1/{}/{}.jpg'
MAX_ALBUMS_ONE_PAGE = 40

INVALID_CHAR = {'\\', '/', ':', '*', '?', '"', '<', '>', '|'}

root_path = '.'

def download_one_album(album_no, directly_download_album=False):
    # Explore image urls.
    html = requests.get(URL_ALBUM.format(album_no)).text.encode('iso-8859-1').decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    max_page = soup.select("#pages a")[-2].text
    album_name = soup.select("title")[0].text.split('_')[0]
    album_name = ''.join(char for char in album_name if char not in INVALID_CHAR)

    html = requests.get(URL_ALBUM.format(album_no) + max_page + '.html')
    soup = BeautifulSoup(html.text, 'lxml')
    last_img = soup.select(".content img")[-1]["src"]

    slash = last_img.rfind('/')
    dot = last_img.rfind('.')

    last_img_no = int(last_img[slash + 1: dot])

    # Download images.
    path = os.path.join(root_path, album_name)
    if not os.path.exists(path): 
        os.makedirs(path)
    elif directly_download_album:
        print('\n* Error: The output folder exists. Exit this program.')
        return

    if directly_download_album:
        print('\n* Info: Start downloading images (album_name: {}).'.format(album_name))

    for i in range(1, last_img_no + 1):
        save_path = os.path.join(path, '{}.jpg'.format(i))
        img = requests.get(IMG.format(album_no, i))

        with open(save_path, 'wb') as img_file:
            img_file.write(img.content)

def download_albums(model_no):
    html = requests.get(URL_MODEL.format(str(model_no))).text.encode('iso-8859-1').decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    albums = soup.select(".hezi ul li >a")
    album_num = int(soup.select(".shoulushuliang span")[0].text)
    model_name = soup.select("title")[0].text.split('_')[0]
    model_name = ''.join(char for char in model_name if char not in INVALID_CHAR)

    global root_path
    root_path = os.path.join('.', model_name)
    if not os.path.exists(root_path): 
        os.makedirs(root_path)
    else:
        print('\n* Error: The output folder exists. Exit this program.')
        return 

    # More than one page.
    page_num = math.ceil(album_num / MAX_ALBUMS_ONE_PAGE)
    if page_num != 1:
        for i in range(1, page_num):
            url = URL_MODEL.format(str(model_no)) + 'index_{}.html'.format(i)
            html = requests.get(url).text.encode('iso-8859-1').decode('utf-8')
            soup = BeautifulSoup(html, 'lxml')
            cur_albums = soup.select(".hezi ul li >a")

            for album in cur_albums:
                albums.append(album)

    print('\n* Info: Finish exploring {} albums (model_name: {}).\n'.format(album_num, model_name))

    pbar = tqdm(total=album_num)
    pbar.set_description("Progress")

    for album in albums:
        slash = album["href"][: -1].rfind('/')
        album_no = album["href"][slash + 1: -1]

        download_one_album(album_no)

        pbar.update(1)

if __name__ == '__main__':
    if DOWNLOAD_FROM_MODEL:
        download_albums(MODEL_NO)
    else:
        download_one_album(ALBUM_NO, True)