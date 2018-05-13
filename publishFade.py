import requests
import re
import json
from PIL import Image
import spider
import time


def send_weibo(pre_str):

    area_to_send = "fade's weibo spiders"

    # 登录fade
    BASE_IP = "https://sysufade.cn/fade_pro/"
    myPW = 'loginUserByTel/13727024851/t123456789'
    r = requests.get(BASE_IP + myPW)
    rjson = r.json()
    print(rjson)

    # 用户信息查询，获取token
    USER_ID = 'getUserById/'
    r = requests.get(BASE_IP + USER_ID + str(rjson.get('user_id')))
    tokenModel = rjson.get("tokenModel")
    rjson = r.json()
    print(rjson)

    # ########################  开始准备发送的数据 #####################
    image_send = {
        "image_coordinate": "0:0",
        "image_cut_size": "1"
    }
    image_array = []

    images_path, text_to_send = get_weibo()

    text_to_send = pre_str + text_to_send
    print("\n\n------")
    print(text_to_send)
    print(images_path)

    # 纯文字的note
    note = {
        "nickname": rjson.get("nickname"),
        "head_image_url": rjson.get("head_image_url"),
        "user_id": str(rjson.get("user_id")),
        "note_content": text_to_send,
        "note_area": area_to_send
    }

    # 获取图片宽高比
    for p in images_path:
        im = Image.open('./images/' + p)
        print(im.size)
        ratio = im.size[0] / im.size[1]
        image_send["image_size"] = str(ratio)
        image_array.append(image_send)

    # 带图片的note
    image_note = {
        "nickname": rjson.get("nickname"),
        "head_image_url": rjson.get("head_image_url"),
        "user_id": str(rjson.get("user_id")),
        "note_content": text_to_send,
        "note_area": area_to_send,
        "images": image_array
    }

    # 判断发送哪种类型的fade
    if len(images_path) > 0:
        file = {"note": json.dumps(image_note)}
    else:
        file = {"note": json.dumps(note)}
    other_file = {"other": ""} # 这个other字段是为了使得纯文字的请求也能以multipart/form-data的形式进行请求
    multiple_files = []

    # 文件（图片）的数据准备
    for img in images_path:
        multiple_files.append(('file', (img, open('./images/' + img, 'rb'), 'image/*')))
    print(multiple_files)

    # 用户token加到请求头
    headers = {'tokenModel': json.dumps(tokenModel)}

    # ########################  结束准备发送的数据 #####################

    # 发送fade
    if len(images_path) > 0:
        r = requests.post(BASE_IP + "addNote", files=multiple_files, data=file, headers=headers)
    else:
        r = requests.post(BASE_IP + "addNote", files=other_file, data=file, headers=headers)
    print(r.text)

    # 退出登录
    r = requests.delete(BASE_IP + "logoutByToken/" + json.dumps(tokenModel))
    print(r.text)


def get_weibo():
    """
    调用爬虫获得微博，包括去重，包括异常情况下的重试
    :return:微博文字，对应的图片路径
    """
    while True:
        try:
            text_to_send, images_path = spider.get_new_weibo()
            historys = open('history.txt', 'r', encoding='utf-8').read()
            if historys.count(text_to_send) > 0:
                print('Error: 内容重复')
                time.sleep(1)
                continue
            else:
                with open('history.txt', 'a', encoding='utf-8') as fo:
                    fo.write(text_to_send + '\n')
        except IndexError as e:
            print(e)
            time.sleep(1)
            continue
        except KeyError as e:
            print(e)
            time.sleep(1)
            continue
        except IOError as e:
            print(e)
            time.sleep(1)
            continue
        except TypeError as e:
            print(e)
            time.sleep(1)
            continue
        except FileNotFoundError as e:
            print(e)
            time.sleep(1)
            continue
        except FileExistsError as e:
            print(e)
            time.sleep(1)
            continue
        else:
            break
    return images_path, text_to_send


if __name__ == '__main__':
    print("--------------------------")
    print(send_weibo(""))
