from multiprocessing import Pool
from Extract_channel import get_channel
from page_parsing import get_info
douban_url = 'https://book.douban.com/'

def get_alllinks(channel):
    for i in range(0, 10000, 20):
        get_info(channel, i)
if __name__ == '__main__':
    pool = Pool()
    pool.map(get_alllinks, get_channel(douban_url).split())
