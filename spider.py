# -*- coding: utf-8 -*-
import requests
import re
import json
from bs4 import BeautifulSoup
from PIL import Image

def getNewWeibo():
    cookit = {
        "Cookit": "_T_WM=7f7181e076eb212385a0de6f757604d5; SSOLoginState=1526026483; ALF=1528618483; SCF=ArxL8HhPfaPJydlRX-jAsdYAkb7yQZRLYUSw96YaJM_eB6uSCtkIqIj7xLzshN_KfXwYQzRsSmCEX7cjL5HJ1QY.; SUB=_2A2538SCjDeRhGeNH6lMT8S_FzTWIHXVVGkDrrDV6PUNbktAKLXmkkW1NSshIildba4uCQXPd7IliRSFzJ0nd528s; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Whdnh1us_LgLSpoQ6FkU4H-5JpX5KzhUgL.Fo-4eK2EeK24So.2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMf1K2peo2p1Kq4; SUHB=0Lcixb7WTY3g6s; WEIBOCN_FROM=1110006030; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D102803%26fid%3D102803%26uicode%3D10000011; MLOGIN=1"}
    datalink = "https://m.weibo.cn/api/container/getIndex?containerid=102803"
    r = requests.get(datalink, cookies=cookit)
    print(r.headers)
    print(r.encoding)
    for i in range(15):
        resjson = r.json()['data']['cards'][i]
        if resjson.get('mblog', -1) != -1:
            resjson = resjson['mblog']  # ['text']
        print(resjson['text'])
        is_valid = False
        pic_names = []
        if resjson.get('pics', -1) != -1:
            for pinfo in resjson.get('pics', -1):
                print(pinfo['large']['url'])
                if not pinfo['large']['url'].endswith('gif'):
                    short_name = pinfo['large']['url'].split('/')[-1]
                    save_path = 'F:\\PY\\fadeRobot\\images\\' + short_name
                    print(save_path)
                    html = requests.get(pinfo['large']['url'])
                    with open(save_path, 'wb') as file:
                        file.write(html.content)
                    is_valid = True
                    pic_names.append(short_name)
            if is_valid:
                text = re.sub(r'<.*>', '', resjson['text'])
                return text, pic_names


if __name__ == '__main__':
    print("--------------------------")
    print(getNewWeibo())
