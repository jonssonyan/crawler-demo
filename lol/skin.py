# !/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import os

import requests

# 设置头部信息，防止被检测出是爬虫
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}
url = "https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js"
# 请求英雄列表的url地址
response = requests.get(url=url, headers=headers).text
loads = json.loads(response)
dic = loads['hero']
for data in dic:
    id_ = data['heroId']
    skinUrl = 'https://game.gtimg.cn/images/lol/act/img/js/hero/%s.js' % id_
    # 请求每个英雄皮肤的url地址
    skinResponse = requests.get(url=skinUrl, headers=headers).text
    json_loads = json.loads(skinResponse)
    hero_ = json_loads['hero']
    save_path = './skin/%s-%s-%s' % (hero_["heroId"], hero_['name'], hero_['title'])
    # 文件夹不存在，则创建文件夹
    folder = os.path.exists(save_path)
    if not folder:
        os.makedirs(save_path)
    skins_ = json_loads['skins']
    for data in skins_:
        if data['chromas'] == '0':
            content = requests.get(url=data['mainImg'], headers=headers).content
            try:
                with open('%s/%s.jpg' % (save_path, data['name']), "wb") as f:
                    print("正在下载英雄：%s 皮肤名称：%s ..." % (hero_['name'], data['name']))
                    f.write(content)
            except Exception as e:
                print('下载失败')
                print(e)
