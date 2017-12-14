# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
douban_url = 'https://book.douban.com/'


def get_channel(url):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    links = soup.select('a.tag')
    for link in links:
        page_url = douban_url + link.get('href')
    return page_url
#get_channel(douban_url)
