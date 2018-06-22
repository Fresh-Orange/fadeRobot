# -*- coding: utf-8 -*-
import requests
import re
import json
from bs4 import BeautifulSoup
from PIL import Image
import random
import urllib


def get_new_weibo():
    """
    获得新的微博（不保证不重复，不保证不产生异常）
    :return: 微博文字，对应的图片路径
    """
    cookit = {
        "Cookit": "_T_WM=3cfa2e469c15b82512c08b1fd741ac1c; ALF=1528621799; SCF=Aqa1yiiIz1eeeiXNlJhf8-e"
                  "hzQ4bryQBxsOHZcsvagx6D0uG4XsiUKlDmL1e597pGstJhq6j7euQZIaISqpJW-E.; SUB=_2A2538S24De"
                  "RhGeNH6lMT8S_FzTWIHXVVHbPwrDV6PUJbktANLUf-kW1NSshIioLDSCIoAZOOx8FsTSwvJrE3_mu0; SUB"
                  "P=0033WrSXqPxfM725Ws9jqgMF55529P9D9Whdnh1us_LgLSpoQ6FkU4H-5JpX5K-hUgL.Fo-4eK2EeK24S"
                  "o.2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMf1K2peo2p1Kq4; SUHB=09PNajWAenMeWC; SSOLoginState"
                  "=1526029800; WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D10000011%"
                  "26lfid%3D100103type%253D1%2526q%253D%2523%25E5%25BE%25AE%25E5%258D%259A%25E7%2583%25"
                  "AD%25E7%2582%25B9%2523%26fid%3D100103type%253D61%2526q%253D%2523%25E5%2588%259B%25E9"
                  "%2580%25A0101%2523%2526t%253D0%26uicode%3D10000011"}

    #topics = ['迪丽热巴', '张艺兴', '刘昊然','赵丽颖','snh48', '蔡徐坤','郑爽','黄婷婷','李艺彤']
    #topics = topics + ['小米', '魅族','iPhone','一加手机', 'OPPO','华为','索尼','锤子科技']
    #topics = topics + ['古风写真','摄影', '手机摄影','旅行摄影','风景', '街拍','旅行','汉服','VSCO','中国图库', '人像摄影']

    topics = getHotSearch()

    # 随机选择话题
    idx = random.randint(0, len(topics)-1)
    #print(idx)
    topic = topics[idx]
    #print(topic)

    datalink = "https://m.weibo.cn/api/container/getIndex?containerid=100103type=61&q=#{topic}#&t=0&page=2".format(topic=topic)
    datalink = urllib.parse.quote(datalink, safe='/:?=')
    #print(datalink)

    r = requests.get(datalink, cookies=cookit)
    #print(r.headers)
    #print(r.encoding)
    for i in range(10):
        resjson = r.json()['data']['cards'][0]
        resjson = resjson['card_group'][i]
        if resjson.get('mblog', -1) != -1:
            resjson = resjson['mblog']
        #print(resjson.get('text', '.'))
        is_valid = False
        pic_names = []
        if resjson.get('pics', -1) != -1:
            for pinfo in resjson.get('pics', -1):
                #print(pinfo['large']['url'])
                # 去掉gif格式的图片
                if not pinfo['large']['url'].endswith('gif'):
                    short_name = pinfo['large']['url'].split('/')[-1]
                    save_path = './images/' + short_name
                    #print(save_path)
                    html = requests.get(pinfo['large']['url'])
                    with open(save_path, 'wb') as file:
                        file.write(html.content)
                    is_valid = True
                    pic_names.append(short_name)
            if is_valid:
                # 用正则表达式去掉可能导致安卓端崩溃的字符
                text = re.sub(r'<.*?>', '', resjson.get('text', '.'))
                text = re.sub(r'\[.*\]', '', text)
                return text, pic_names
    return "",[]

def getHotSearch():
    link = "https://m.weibo.cn/api/container/getIndex?containerid=106003" \
           "type%253D25%2526t%253D3%2526disable_hot%253D1%2526filter_type%253" \
           "Drealtimehot&title=%25E5%25BE%25AE%25E5%258D%259A%25E7%2583%25AD%25E6%2590%259C&" \
           "extparam=filter_type%3Drealtimehot%26mi_cid%3D%26pos%3D0_0%26c_type%3D30%26" \
           "display_time%3D1529662849&luicode=10000011&lfid=106003type%3D1"
    r = requests.get(link)
    #print(r.headers)
    #print(r.encoding)
    words_list = []
    for i in range(20):
        resjson = r.json()['data']['cards'][0]
        resjson = resjson['card_group'][i]
        if resjson.get('desc', -1) != -1:
            word = resjson['desc']
            words_list.append(word)
    #print("热搜词",words_list)
    return words_list


if __name__ == '__main__':
    #print("--------------------------")
    print(get_new_weibo())