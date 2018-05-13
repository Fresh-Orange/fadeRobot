import time
import publishFade

while True:
    publishFade.send_weibo("")
    time.sleep(60*30) # 每隔30分钟运行一次
