# coding: UTF-8
"""
user: 五根弦的吉他
function: 单进程爬取淘宝商品信息并保存
使用方法：1、找到keyword变量改成自己想要的东西；
        2、找到collection_name变量选择在taobao数据库里要新建的集合名
time：2019-3-19

"""

from selenium import webdriver
from urllib.parse import quote
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
import pymongo
import json
import time
import random
from datetime import datetime
from multiprocessing.pool import Pool


"""
cookies = [
{
    "domain": ".taobao.com",
    "expirationDate": 1584728973.434377,
    "hostOnly": "false",
    "httpOnly": "false",
    "name": "_cc_",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": "false",
    "session": "false",
    "storeId": "0",
    "value": "VFC%2FuZ9ajQ%3D%3D",
    "id": 1
},
{
    "domain": ".taobao.com",
    "hostOnly": "false",
    "httpOnly": "false",
    "name": "_l_g_",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": "false",
    "session": "true",
    "storeId": "0",
    "value": "Ug%3D%3D",
    "id": 2
},
{
    "domain": ".taobao.com",
    "hostOnly": "false",
    "httpOnly": "false",
    "name": "_nk_",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": "false",
    "session": "true",
    "storeId": "0",
    "value": "%5Cu7693%5Cu6708%5Cu661F%5Cu7A7A922",
    "id": 3
},
{
    "domain": ".taobao.com",
    "hostOnly": "false",
    "httpOnly": "false",
    "name": "_tb_token_",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": "false",
    "session": "true",
    "storeId": "0",
    "value": "7e71658335e36",
    "id": 4
},
{
    "domain": ".taobao.com",
    "expirationDate": 2183717422,
    "hostOnly": "false",
    "httpOnly": "false",
    "name": "cna",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": "false",
    "session": "false",
    "storeId": "0",
    "value": "LsoXFdYeJm4CAXGMC3v2KLsT",
    "id": 5
},
{
    "domain": ".taobao.com",
    "hostOnly": "false",
    "httpOnly": "true",
    "name": "cookie1",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": "false",
    "session": "true",
    "storeId": "0",
    "value": "BxT4il3gacTIptM%2FX7T0yagooXjswkMVP%2BSPduPQTy4%3D",
    "id": 6
},
{
    "domain": ".taobao.com",
    "hostOnly": "false",
    "httpOnly": "true",
    "name": "cookie17",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": "false",
    "session": "true",
    "storeId": "0",
    "value": "UUGk3pPgSqKa2Q%3D%3D",
    "id": 7
},
{
    "domain": ".taobao.com",
    "hostOnly": "false",
    "httpOnly": "true",
    "name": "cookie2",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": "false",
    "session": "true",
    "storeId": "0",
    "value": "1825d449bd351e416e4f3144ba9ab666",
    "id": 8
},
{
    "domain": ".taobao.com",
    "hostOnly": "false",
    "httpOnly": "false",
    "name": "csg",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": "false",
    "session": "true",
    "storeId": "0",
    "value": "a83ec6c3",
    "id": 9
},
{
    "domain": ".taobao.com",
    "hostOnly": "false",
    "httpOnly": "false",
    "name": "dnk",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": "false",
    "session": "true",
    "storeId": "0",
    "value": "%5Cu7693%5Cu6708%5Cu661F%5Cu7A7A922",
    "id": 10
},
{
    "domain": ".taobao.com",
    "expirationDate": 1868435437.132287,
    "hostOnly": "false",
    "httpOnly": "true",
    "name": "enc",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": "true",
    "session": "false",
    "storeId": "0",
    "value": "idpcwypnUnn%2BSxrP8JjkoI19oZem4SzYe%2FH5Nur%2BdBFWc00ioEx5I4srXNV0Pa7BvhWU74PNwc59zoc1yWrTQg%3D%3D",
    "id": 11
},
{
    "domain": ".taobao.com",
    "hostOnly": "false",
    "httpOnly": "false",
    "name": "existShop",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": "false",
    "session": "true",
    "storeId": "0",
    "value": "MTU1MzE5Mjk3Mw%3D%3D",
    "id": 12
},
{
    "domain": ".taobao.com",
    "expirationDate": 1584663214.798886,
    "hostOnly": "false",
    "httpOnly": "false",
    "name": "hng",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": "false",
    "session": "false",
    "storeId": "0",
    "value": "CN%7Czh-CN%7CCNY%7C156",
    "id": 13
},
{
    "domain": ".taobao.com",
    "expirationDate": 1568744974,
    "hostOnly": "false",
    "httpOnly": "false",
    "name": "isg",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": "false",
    "session": "false",
    "storeId": "0",
    "value": "BBkZNjNzoRu_RX2Md1PfbpsbKAwzDibybh7bMTvOlcC_QjnUg_YdKIdQRUaRCqWQ",
    "id": 14
},
{
    "domain": ".taobao.com",
    "expirationDate": 1568744975,
    "hostOnly": "false",
    "httpOnly": "false",
    "name": "l",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": "false",
    "session": "false",
    "storeId": "0",
    "value": "bBrdlj6IvoTFU-vyBOCanurza77OSIRYYuPzaNbMi_5CQ6T1cPbOltVGgF96Vj5RsDTB43ExOeJ9-eteZ",
    "id": 15
},
{
    "domain": ".taobao.com",
    "expirationDate": 1555784973.43424,
    "hostOnly": "false",
    "httpOnly": "false",
    "name": "lgc",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": "false",
    "session": "false",
    "storeId": "0",
    "value": "%5Cu7693%5Cu6708%5Cu661F%5Cu7A7A922",
    "id": 16
},
{
    "domain": ".taobao.com",
    "expirationDate": 1553797773.434988,
    "hostOnly": "false",
    "httpOnly": "false",
    "name": "mt",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": "false",
    "session": "false",
    "storeId": "0",
    "value": "ci=119_1&np=",
    "id": 17
},
{
    "domain": ".taobao.com",
    "hostOnly": "false",
    "httpOnly": "false",
    "name": "sg",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": "false",
    "session": "true",
    "storeId": "0",
    "value": "290",
    "id": 18
},
{
    "domain": ".taobao.com",
    "hostOnly": "false",
    "httpOnly": "true",
    "name": "skt",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": "false",
    "session": "true",
    "storeId": "0",
    "value": "f777bc52787fae0f",
    "id": 19
},
{
    "domain": ".taobao.com",
    "expirationDate": 1560968973.431556,
    "hostOnly": "false",
    "httpOnly": "false",
    "name": "t",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": "false",
    "session": "false",
    "storeId": "0",
    "value": "788cd7f28f14a318b448f6261561e8ff",
    "id": 20
},
{
    "domain": ".taobao.com",
    "expirationDate": 1607192973.434817,
    "hostOnly": "false",
    "httpOnly": "false",
    "name": "tg",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": "false",
    "session": "false",
    "storeId": "0",
    "value": "0",
    "id": 21
},
{
    "domain": ".taobao.com",
    "expirationDate": 1584101433,
    "hostOnly": "false",
    "httpOnly": "false",
    "name": "thw",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": "false",
    "session": "false",
    "storeId": "0",
    "value": "cn",
    "id": 22
},
{
    "domain": ".taobao.com",
    "expirationDate": 1584728973.434081,
    "hostOnly": "false",
    "httpOnly": "false",
    "name": "tracknick",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": "false",
    "session": "false",
    "storeId": "0",
    "value": "%5Cu7693%5Cu6708%5Cu661F%5Cu7A7A922",
    "id": 23
},
{
    "domain": ".taobao.com",
    "hostOnly": "false",
    "httpOnly": "false",
    "name": "uc1",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": "false",
    "session": "true",
    "storeId": "0",
    "value": "cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D&cookie21=VFC%2FuZ9aiKCaj7AzMHh1&cookie15=U%2BGCWk%2F75gdr5Q%3D%3D&existShop=false&pas=0&cookie14=UoTZ50jBHCv9bQ%3D%3D&tag=8&lng=zh_CN",
    "id": 24
},
{
    "domain": ".taobao.com",
    "expirationDate": 1555784973.433728,
    "hostOnly": "false",
    "httpOnly": "true",
    "name": "uc3",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": "false",
    "session": "false",
    "storeId": "0",
    "value": "vt3=F8dByErXGyctPnBQumA%3D&id2=UUGk3pPgSqKa2Q%3D%3D&nk2=k1HLL0Ln8XbZeAE%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D",
    "id": 25
},
{
    "domain": ".taobao.com",
    "expirationDate": 1568882439,
    "hostOnly": "false",
    "httpOnly": "false",
    "name": "UM_distinctid",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": "false",
    "session": "false",
    "storeId": "0",
    "value": "1699f68cc77b17-0cfd2708c3cb11-3e740b5c-100200-1699f68cc789f5",
    "id": 26
},
{
    "domain": ".taobao.com",
    "hostOnly": "false",
    "httpOnly": "true",
    "name": "unb",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": "false",
    "session": "true",
    "storeId": "0",
    "value": "2960458799",
    "id": 27
},
{
    "domain": ".taobao.com",
    "hostOnly": "false",
    "httpOnly": "false",
    "name": "v",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": "false",
    "session": "true",
    "storeId": "0",
    "value": "0",
    "id": 28
},
{
    "domain": ".taobao.com",
    "expirationDate": 1584728934,
    "hostOnly": "false",
    "httpOnly": "false",
    "name": "x",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": "false",
    "session": "false",
    "storeId": "0",
    "value": "e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0",
    "id": 29
},
{
    "domain": "i.taobao.com",
    "expirationDate": 1553196574.22964,
    "hostOnly": "true",
    "httpOnly": "true",
    "name": "_mw_us_time_",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": "true",
    "session": "false",
    "storeId": "0",
    "value": "1553192974447",
    "id": 30
}
]

"""
# 爬取页数
page_total = 100

# 为chrome开启实验性功能参数(防止window.navigator.webdriver参数是true，被发现是selenium控制)
option = webdriver.ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])


browser = webdriver.Chrome(options=option)

"""
# 添加淘宝的cookie
for i in cookies:
    browser.add_cookie(i)
"""

#browser.implicitly_wait(10)
wait = WebDriverWait(browser, 10)
keyword = '女装卫衣'                             # 要找的物品关键字
base_url = 'https://s.taobao.com/search?q='

mong_ip = 'localhost'
db_name = 'taobao'     # 指定要操作的数据库（要提前创建好）
collection_name = 'girl_fleece'   # 要新建的集合名
#client = pymongo.MongoClient(host=mong_ip)  # port默认为27017
client = pymongo.MongoClient('mongodb://again:cgh111@localhost:27017/')  # 连上mongo超级用户
db = client[db_name]
collection = db[collection_name]


def save2mongo(data):

    try:
        if collection.insert_one(data):
            print('Successfully inset data!')

    except Exception:
        print('Failed insert!')


def get_info():
    """
    function: 爬取该页面所有商品
    """
    doc = pq(browser.page_source)
    items = doc('.m-itemlist .items .item').items()

    for item in items:
        data = {
            'image': item.find('.pic .img').attr('src'),
            #'price': item.find('div.price').text(),
            'price': item.find('.price').text().replace('\n', ''),
            #'buyers_num': item.find('div.deal-cnt').text().replace('人付款', ''),
            'buyers_num': item.find('.deal-cnt').text().replace('人付款', ''),
            #'description': item.find('div.row.row-2.title').text(),
            'description': item.find('.row.row-2.title').text().replace('\n',''),
            #'shop': item.find('div.shop span').text(),
            'shop': item.find('.shop').text(),
            #'location': item.find('div.location').text()
            'location': item.find('.location').text()

        }
        print(data)

        with open('data2.json', 'a+', encoding='utf-8 ') as f:   # 记得文件要加字符编码，为了输出中文，需指定参数ensure_ascii
            f.write(json.dumps(data, indent=2, ensure_ascii=False)+',\n')  # json文件的缩进与ensure_ascii
            print('写入成功')

        save2mongo(data)


def jump2page(page):

    try:
        browser.get(url=base_url + quote(keyword))
        time.sleep(random.uniform(1, 2.5))

        # 下拉进度条，模拟行为
        #js = "var q=document.documentElement.scrollTop={}".format(random.random(100, 900))       # 下拉100个像素
        browser.execute_script('window.scrollTo(0, 500)')
        time.sleep(1)

        # 判断是否要跳转下一页
        if page > 1:
            # until()方法找到节点成功就返回该节点，否则返回异常
            input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.form > input.input.J_Input')))  # 注意传入的是元组定位节点参数
            submit_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.form > .btn.J_Submit')))

            input.clear()
            input.send_keys(page)
            time.sleep(random.uniform(1, 2.5))
            submit_btn.click()

        # 通过显示的高亮页码数字判断是否跳转成功
        # text_to_be_present_in_element((参数), 期望值)方法是判断节点文本是否与期望值相同，返回布尔值
        shine = wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager ul.items .item.active span'), str(page)))

        # 检查该页面是否已加载出商品节点信息，若无问题则后面就能放心取源码来爬取（其实后面再判断也可以）
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))

        # 爬取商品
        print('开始爬取商品')
        get_info()

    except Exception:
        jump2page(page)


# 单线程
def main():
    for page in ListPage:
        jump2page(page)


'''
# 多线程
def main(page):
    jump2page(page)
'''


if __name__ == '__main__':
    start = datetime.now()
    ListPage = range(1, page_total)

    # 单线程
    main()

    """
    # 多线程
    pool = Pool()
    pool.map(main, ListPage)
    pool.close()
    pool.join()
    """

    end = datetime.now()
    browser.close()
    print('\n'+'='*50+'DONE! Duration:', end-start)
