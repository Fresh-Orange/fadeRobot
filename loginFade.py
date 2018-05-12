import requests
import re
import json
from PIL import Image
import spider

def sendWeibo(pre_str):
    # text_to_send = "fade机器人发图片啦，拜托让我发成功吧"
    area_to_send = "fade's weibo spiders"

    BASE_IP = "https://sysufade.cn/fade_pro/"
    myPW = 'loginUserByTel/13727024851/t123456789'
    r = requests.get(BASE_IP + myPW)

    rjson = r.json()
    print(rjson)

    USER_ID = 'getUserById/'
    r = requests.get(BASE_IP + USER_ID + str(rjson.get('user_id')))
    tokenModel = rjson.get("tokenModel")
    rjson = r.json()
    print(rjson)

    image_send = {
        "image_coordinate": "0:0",
        "image_cut_size": "1"
    }
    image_array = []

    text_to_send, images_path = spider.getNewWeibo()
    text_to_send = pre_str + text_to_send
    print("\n\n------")
    print(text_to_send)
    print(images_path)

    note = {
        "nickname": rjson.get("nickname"),
        "head_image_url": rjson.get("head_image_url"),
        "user_id": str(rjson.get("user_id")),
        "note_content": text_to_send,
        "note_area": area_to_send
    }

    for p in images_path:
        im = Image.open('F:\\PY\\fadeRobot\\images\\' + p)
        print(im.size)
        ratio = im.size[0] / im.size[1]
        image_send["image_size"] = str(ratio)
        image_array.append(image_send)

    image_note = {
        "nickname": rjson.get("nickname"),
        "head_image_url": rjson.get("head_image_url"),
        "user_id": str(rjson.get("user_id")),
        "note_content": text_to_send,
        "note_area": area_to_send,
        "images": image_array
    }

    if len(images_path) > 0:
        file = {"note": json.dumps(image_note)}
    else:
        file = {"note": json.dumps(note)}
    other_file = {"other": ""}
    multiple_files = []
    for img in images_path:
        multiple_files.append(('file', (img, open('F:\\PY\\fadeRobot\\images\\' + img, 'rb'), 'image/*')))

    print(multiple_files)

    headers = {'tokenModel': json.dumps(tokenModel)}

    if len(images_path) > 0:
        r = requests.post(BASE_IP + "addNote", files=multiple_files, data=file, headers=headers)
    else:
        r = requests.post(BASE_IP + "addNote", files=other_file, data=file, headers=headers)
    print(r.text)

    r = requests.delete(BASE_IP + "logoutByToken/" + json.dumps(tokenModel))
    print(r.text)
