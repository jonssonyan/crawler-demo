# !/usr/bin/python
# -*- coding: UTF-8 -*-
import os

import requests
from lxml import etree

# 设置头部信息，防止被检测出是爬虫
headers = {
    'Host': 'movie.douban.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}

id = input('请输入电影id：')
page = int(input('请输入爬取的页数：'))

# 循环请求接口
for i in range(0, page):
    # 循环请求每页的数据
    re = requests.get(
        url='https://movie.douban.com/subject/%s/comments?start=%d&limit=20&sort=new_score&status=P' % (id, 20 * i),
        headers=headers).text
    # 构造了一个XPath解析对象并对HTML文本进行自动修正
    html = etree.HTML(re)
    # XPath使用路径表达式来选取用户名
    comment = html.xpath('//div[@class="comment"]')
    for content in comment:
        names = content.xpath('.//a[@class=""]')
        grades = content.xpath('.//span[contains(@class,"rating")]')
        texts = content.xpath('.//span[@class="short"]')
        name = names[0].xpath('./text()')[0]
        if len(grades) > 0:
            grade = grades[0].xpath('./@class')[0][7:8] + '星'
        else:
            grade = '暂无评价'
        text = texts[0].xpath('./text()')[0]
        # 文件夹不存在，则创建文件夹
        save_path = './douban'
        folder = os.path.exists(save_path)
        if not folder:
            os.makedirs(save_path)
        with open('./douban/comments.text', 'a+', encoding='utf-8') as f:
            f.write('用户名：%s\n' % name)
            f.write('评价：%s\n' % grade)
            f.write('评论内容：%s\n' % text)
            f.write('==========================================================================\n')
