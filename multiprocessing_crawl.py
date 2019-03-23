# coding: UTF-8
import requests
import re
import time
from datetime import datetime
from urllib.parse import urlencode
import pymongo
from multiprocessing.pool import Pool


keyword = '女生包包'
db_name = 'taobao'
collection_name = 'bao'
total_page = 100

base_url = 'https://s.taobao.com/search'

#client = pymongo.MongoClient("mongodb://YourUser:yourpwd@localhost:27017/")
client = pymongo.MongoClient('mongodb://YourUser:yourpwd@localhost:27017/')  # 连上mongo超级用户
db = client[db_name]
collection = db[collection_name]


def get_TimeSpan():

    t = str(time.time()).split('.')

    latter_list = [i for i in t[1]]  # 把字符串分成一个个字符

    to_former = ''.join(latter_list[:3])
    del latter_list[:3]
    latter = ''.join(latter_list)


    former = t[0] + to_former

    #print('final: {former}_{latter}'.format(former=former, latter=latter))

    ts = '{former}_{latter}'.format(former=former, latter=latter)

    return ts


def save_data(dict_data):
    if collection.insert_one(dict_data):
        print('插入成功')


def get_info(jdata):
    for item in jdata.get("mods").get("itemlist").get("data").get("auctions"):
        dict_data = {
            'nick': item["nick"],
            'location': item["item_loc"],
            'title': re.sub('[A-Za-z0-9\!\%\[\]\,\。\<\>\=\s]', '', item["title"]),
            'price': item["view_price"],
            'comment_count': item["comment_count"],
            'comment_url': item["comment_url"].strip(),
            'paid_people': item["view_sales"].replace('人付款', ''),
            'pic_url': item["pic_url"].strip(),
            'detail_url': item["detail_url"],
            'shopLink': item["shopLink"],

        }
        print("*"*50+'\n', dict_data)
        save_data(dict_data)


def get_page(d_v, ts, bcoffset, ntoffset, s):
    #"https://s.taobao.com/search?data-key=s&data-value=88&ajax=true&_ksTS=1553315509048_1083&callback=jsonp1084&q=%E5%A5%B3%E7%94%9F%E5%8C%85%E5%8C%85&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&bcoffset=0&ntoffset=6&p4ppushleft=1%2C48&s=44"
    params = {
        'data-key': 's',
        'data-value': d_v,
        'ajax': 'true',
        '_ksTS': ts,
        'q': keyword,
        'imgfile': '',
        'commend': 'all',
        'ssid': 's5-e',
        'search_type': 'item',
        'sourceId': 'tb.index',
        'spm': 'a21bo.2017.201856-taobao-item.1',
        'ie': 'utf8',
        'initiative_id': 'tbindexz_20170306',
        'bcoffset': bcoffset,
        'ntoffset': ntoffset,
        'p4ppushleft': '1%2C48',
        's': s

    }

    #url = base_url + urlencode(params)

    try:
        response = requests.get(base_url, params)
        if response.status_code == 200:
            jdata = response.json()
            response.close()
            #jdata.get("mods").get("itemlist")
            get_info(jdata)

    except Exception:
        print("Retry!")
        get_page(d_v, ts, bcoffset, ntoffset, s)


def main(page):
    d_v = page * 44
    ts = get_TimeSpan()
    bcoffset = 3 - 3 * (page - 1)
    ntoffset = 9 - 3 * (page - 1)
    s = 44 * (page - 1)
    get_page(d_v, ts, bcoffset, ntoffset, s)


if __name__ == '__main__':
    start = datetime.now()

    pool = Pool()

    PageList = [i for i in range(1, total_page)]
    pool.map(main, PageList)
    pool.close()
    pool.close()

    end = datetime.now()
    print("DONE! Duration:", end-start)
