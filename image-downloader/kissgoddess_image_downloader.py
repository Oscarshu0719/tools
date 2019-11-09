# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import os
import requests
from tqdm import tqdm


"""
    Image downloader of https://kissgoddess.com/.

    Usage: 
        python kissgoddess_image_downloader.py

    Notice:
        `MODEL_NAME`, `ALBUM_NO` and `DOWNLOAD_FROM_MODEL` are changeable.
"""

URL_ALBUM = 'https://kissgoddess.com/album/{}{}.html'
URL_MODEL = 'https://kissgoddess.com/people/{}.html'
URL_VIEW_MORE = 'https://kissgoddess.com/ajax/person_album_handle.ashx?id={}'

# Change `MODEL_NAME` to specify different model.
MODEL_NAME = 'jun-amaki'
# Change `ALBUM_NO` to specify different album.
ALBUM_NO = 26497
"""
DOWNLOAD_FROM_MODEL: 
    True: Download all albums of a model.
    False: Download only one album.
"""
DOWNLOAD_FROM_MODEL = False

INVALID_CHAR = {'\\', '/', ':', '*', '?', '"', '<', '>', '|'}

root_path = '.'

def download_one_album(album_no, directly_download_album=False):
    first_page_flag = True

    index = 1
    img_dict = dict()
    img_dict['url'] = list()
    img_dict['name'] = list()

    # Explore image urls.
    while True:
        if first_page_flag:
            html = requests.get(URL_ALBUM.format(album_no, ''))
            first_page_flag = False
        else:
            html = requests.get(URL_ALBUM.format(album_no, '_' + str(index)))
            index += 1
        if html.status_code == 404:
            break

        soup = BeautifulSoup(html.text, 'lxml')
        imgs = soup.select(".td-gallery-content img")

        for img in imgs:
            img_dict['url'].append(img["src"])
            img_dict['name'].append(img["alt"])

    # Download images.
    underline = img_dict['name'][0].rfind('_')
    album_name = img_dict['name'][0][: underline]
    album_name = ''.join(char for char in album_name if char not in INVALID_CHAR)
    path = os.path.join(root_path, album_name)

    if not os.path.exists(path): 
        os.makedirs(path)
    elif directly_download_album:
        print('\n* Error: The output folder exists. Exit this program.')
        return

    if directly_download_album:
        print('\n* Info: Start downloading images (album_name: {}).'.format(album_name))

    for i in range(len(img_dict['url'])):
        save_path = os.path.join(path, str(i + 1) + '.jpg')
        img = requests.get(img_dict['url'][i])

        with open(save_path, 'wb') as img_file:
            img_file.write(img.content)

def download_albums(model_name):
    html = requests.get(URL_MODEL.format(model_name))
    soup = BeautifulSoup(html.text, 'lxml')
    btn_view_more = soup.find("meta", property="og:image")
    model_real_name = soup.select(".person-name")[0].text
    model_real_name = ''.join(char for char in model_real_name if char not in INVALID_CHAR)

    slash = btn_view_more["content"].rfind('/')
    dot = btn_view_more["content"].rfind('.')
    model_id = btn_view_more["content"][slash + 1: dot]

    tmp_albums = soup.select(".td-module-thumb a")
    albums = set()
    for album in tmp_albums:
        slash = album["href"].rfind('/')
        dot = album["href"].rfind('.')
        album_no = album["href"][slash + 1: dot]
        albums.add(album_no)

    html = requests.get(URL_VIEW_MORE.format(model_id))
    soup = BeautifulSoup(html.text, 'lxml')

    more_albums = soup.select(".td-module-thumb a")

    global root_path
    root_path = os.path.join('.', model_real_name)
    if not os.path.exists(root_path): 
        os.makedirs(root_path)
    else:
        print('\n* Error: The output folder exists. Exit this program.')
        return

    for album in more_albums:
        slash = album["href"].rfind('/')
        dot = album["href"].rfind('.')
        album_no = album["href"][slash + 1: dot]
        albums.add(album_no)

    print("\n* Info: Finish exploring {} albums (model_real_name: {}).\n".format(len(albums), model_real_name))

    pbar = tqdm(total=len(albums))
    pbar.set_description("Progress")

    for album_no in albums:
        download_one_album(album_no)
        
        pbar.update(1)

if __name__ == '__main__':
    if DOWNLOAD_FROM_MODEL:
        download_albums(MODEL_NAME)
    else:
        download_one_album(ALBUM_NO, True)
