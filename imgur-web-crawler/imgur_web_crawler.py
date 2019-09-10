# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re
import os
import sys
import re
import requests
from selenium import webdriver


"""
    Usage:
        python imgur_web_crawler.py [path [option]]
    
    Args:
        path: Input path (can be a folder or a file or an url).
            (Default: Current folder.)
        option: 0 or 1; 
            0 indicates non-recursive, and 1 indicates recursive.
            (Default: 0.)
    
    Notice:
        Put the chromedriver.exe in the same folder.
"""

SAVE_PATH = '.\\imgur'
CHROME_DRIVER_PATH = '.\\chromedriver.exe'
pattern_reddit_url = r'^https?://i.redd.it'
pattern_imgur_url_1 = r'^https?://i.imgur.com'
pattern_imgur_url_2 = r'^https?://imgur.com'
pattern_input_file = r'*.txt'

def find_urls(path, option):
    print('Start exploring urls in files ...\n')

    urls = list()
    urls_dynamic = list()

    # Save all urls from folders or files.
    # An url in imgur pattern 1.
    if re.match(pattern_imgur_url_1, path) or re.match(pattern_reddit_url, path):
        urls.append(path)
    # An url in imgur pattern 2.
    elif re.match(pattern_imgur_url_2, path):
        urls_dynamic.append(path.strip())
    # A file.
    elif os.path.isfile(path):
        with open(path, 'r', encoding='utf8') as input_file:
            for line in input_file:
                if re.match(pattern_imgur_url_1, line) or re.match(pattern_reddit_url, line):
                    urls.append(line.strip())
                elif re.match(pattern_imgur_url_2, line):
                    urls_dynamic.append(line.strip())
    # A folder.
    elif os.path.isdir(path):
        # Include subfolders.
        if option == 1:
            for root, dirs, files in os.walk(path):
                for file in files:
                    filename = os.path.join(root, file)
                    if re.match(pattern_input_file, filename):
                        with open(filename, 'r', encoding='utf8') as input_file:
                            for line in input_file:
                                if re.match(pattern_imgur_url_1, line) or re.match(pattern_reddit_url, line):
                                    urls.append(line.strip())
                                elif re.match(pattern_imgur_url_2, line):
                                    urls_dynamic.append(line.strip())
        # Only current folder.
        elif option == 0:
            for file in os.listdir(path):
                filename = os.path.join(path, file)
                if os.path.isfile(filename) and re.match(pattern_input_file, filename):
                    with open(filename, 'r', encoding='utf8') as input_file:
                        for line in input_file:
                            if re.match(pattern_imgur_url_1, line) or re.match(pattern_reddit_url, line):
                                urls.append(line.strip())
                            elif re.match(pattern_imgur_url_2, line):
                                urls_dynamic.append(line.strip())

    trans_dynamic_urls = dynamic_crawler(urls_dynamic)

    for url in trans_dynamic_urls:
        urls.append(url)

    print('Finish exploring urls ...\n')

    return urls

def dynamic_crawler(urls):
    browser = webdriver.Chrome(CHROME_DRIVER_PATH)
    
    trans_dynamic_urls = list()
    for url in urls:
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        for ele in soup.select("[class='image post-image'] div img"):
            trans_dynamic_urls.append(ele['src'])
    browser.close()

    return trans_dynamic_urls
    
def save_images(urls):
    print('Start saving images ...\n')

    # Save images.
    img_count = 1
    for url in urls:
        index = url.rfind('/')
        pic_name = url[index + 1:]

        save_path = os.path.join(SAVE_PATH, pic_name)
        pic = requests.get(url)
        with open(save_path, 'wb') as img:
            img.write(pic.content)

        img_count += 1 

    print('Finish saving images ...\n')

if __name__ == '__main__':
    url_path = '.'
    option = 0

    if len(sys.argv) == 2:
        url_path = sys.argv[1]
    elif len(sys.argv) == 3:
        url_path = sys.argv[1]
        option = sys.argv[2]

    assert option != 0 or option != 1, 'Illegal option value: ' + option

    if not os.path.exists(SAVE_PATH): 
        os.makedirs(SAVE_PATH)
    
    urls = find_urls(path=url_path, option=option)

    save_images(urls)
