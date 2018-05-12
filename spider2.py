import requests
import time
from bs4 import BeautifulSoup



headers = {
    'Cookie': 'ALF=1528621799; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Whdnh1us_LgLSpoQ6FkU4H-5JpX5K-hUgL.Fo-4eK2EeK24So.2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMf1K2peo2p1Kq4; SUHB=09PNajWAenMeWC; SSOLoginState=1526029800; MLOGIN=1',
    'Host': 'm.weibo.cn',
    'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01'
    }

# change 1632069872
r = requests.get('http://m.weibo.cn/u/1632069872', headers=headers)
soup = BeautifulSoup(r.text)
print(soup)
containerid = soup.find_all('script')[1].get_text()[42:58]


f = open('1.txt', 'a')
i = 1
while True:
    r = requests.get(
        'http://m.weibo.cn/page/json?containerid=' + str(containerid) + '_-_WEIBO_SECOND_PROFILE_WEIBO&page=' + str(i),
        headers=headers)
    card_group = r.json()['cards'][0]['card_group']
    for card in card_group:
        f.write(card['mblog']['text'])
        f.write('\n')
    i = i + 1
    print
    i
    time.sleep(10)