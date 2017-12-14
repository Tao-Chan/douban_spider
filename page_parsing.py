from bs4 import BeautifulSoup
import requests
import time
import pymongo
import re
import random
hds = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
proxy_list = [
    'http://111.13.7.42',
    'http://61.153.67.110',
    'http://101.200.129.250',
]
proxy_ip = random.choice(proxy_list)
proxies = {'http': proxy_ip}

client = pymongo.MongoClient('localhost', 27017)
douban = client['douban']
info = douban['info']
def get_info(channel,page):
    douban = requests.get(('{}?start={}&type=T'.format(channel, str(page))), headers=hds, proxies=proxies)
    time.sleep(2)
    soup = BeautifulSoup(douban.text, 'lxml')
    if soup.select('div.info'):
        titles = soup.select('div.info > h2 > a')
        bookurl = soup.select('div.info > h2 > a')
        deses = soup.select('div.info > div.pub')
        ratings = soup.select('span.rating_nums')
        for title, url, des, rating in zip(titles, bookurl, deses, ratings):
            data = {
                '地址': url.get('href')
            }
            titlelist = []
            for stitle in re.split(r'\+s', title.get_text()):
                titlelist.append(stitle.strip())
                data['书名'] = titlelist
                try:
                    authorlist = []
                    for author in des.get_text().split('/')[0:-3]:
                        authorlist.append(author.strip())
                        data['作者/译者'] = authorlist
                except None:
                     data['作者/译者'] = '暂无'
                try:
                    data['出版社'] = des.get_text().split('/')[-3].strip()
                except:
                    data['出版社'] = '暂无'
                try:
                    data['价格'] = des.get_text().split('/')[-1].strip()
                except:
                    data['价格'] = '暂无'
                try:
                    data['评分'] = rating.get_text()
                except:
                    data['评分'] = '暂无'
            info.insert_one(data)
            print(data)
        print('Genius!')
    else:
        pass
        #info.insert_one(data)
get_info('https://book.douban.com//tag/小说', 20)
