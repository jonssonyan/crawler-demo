# !/usr/bin/python
# -*- coding: UTF-8 -*-
import argparse
import os

import requests
import xlsxwriter
from lxml import etree

# 请求微信文章的头部信息
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Host': 'weixin.sogou.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
}
# 下载图片的头部信息
headers_images = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Host': 'img01.sogoucdn.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
}
count = 0
all = []
# 接收程序传来的参数
parser = argparse.ArgumentParser()
parser.add_argument('-path', dest="path",
                    type=str, required=False,
                    default="", help="文件输出的路径，默认为当前目录")
parser.add_argument('-num', dest="num",
                    type=int, required=False,
                    default=20, help="文章的个数（20的倍数），默认为20篇")
args = parser.parse_args()
# 文件根目录
save_path = './微信文章'
if args.path.strip() != '':
    save_path = args.path
folder = os.path.exists(save_path)
if not folder:
    os.makedirs(save_path)
# 创建图片文件夹
images_path = '%s/图片' % save_path
folder = os.path.exists(images_path)
if not folder:
    os.makedirs(images_path)
num = args.num
num_1 = 1
num_2 = 2
# 文章数量最大为3600
if num > 3600:
    num = 3600
else:
    min = 3600
    for a in range(1, 21):
        for b in range(2, 11):
            min_ = abs(a * (b - 1) * 20 - num)
            if min_ == 0:
                num_1 = a
                num_2 = b
                break
            if min_ < min:
                min = min_
                num_1 = a
                num_2 = b
        else:
            continue
        break
for i in range(0, num_1):
    for j in range(1, num_2):
        url = "https://weixin.sogou.com/pcindex/pc/pc_%d/%d.html" % (i, j)
        # 请求搜狗文章的url地址
        try:
            response = requests.get(url=url, headers=headers, timeout=5).text.encode('iso-8859-1').decode('utf-8')
        except requests.exceptions.RequestException as e:
            print("请求异常：%s", e)
            break
        # 构造了一个XPath解析对象并对HTML文本进行自动修正
        html = etree.HTML(response)
        # XPath使用路径表达式来选取用户名
        xpath = html.xpath('/html/body/li')
        for content in xpath:
            # 计数
            count = count + 1
            # 文章标题
            title = content.xpath('./div[@class="txt-box"]/h3//text()')[0]
            author_ = content.xpath('./div[@class="txt-box"]/div/a//text()')
            article = {}
            # 作者存在
            if author_:
                article['title'] = title
                article['id'] = '%d.jpg' % count
                article['author'] = author_
                # 图片路径
                path = 'http:' + content.xpath('./div[@class="img-box"]//img/@src')[0]
                # 下载文章图片
                try:
                    images = requests.get(url=path, headers=headers_images, timeout=5).content
                except requests.exceptions.RequestException as e:
                    print("请求异常：%s", e)
                    break
                try:
                    with open('%s/%d.jpg' % (images_path, count), "wb") as f:
                        print('正在下载第%d篇文章图片' % count)
                        f.write(images)
                        all.append(article)
                except Exception as e:
                    print('下载文章图片失败：%s' % e)
# 信息存储在excel中
if len(all) > 0:
    # 创建一个workbookx
    workbook = xlsxwriter.Workbook('%s/Excel格式.xlsx' % save_path)
    # 创建一个worksheet
    worksheet = workbook.add_worksheet()
    print('正在生成Excel...')
    try:
        for i in range(0, len(all) + 1):
            # 第一行用于写入表头
            if i == 0:
                worksheet.write(i, 0, 'title')
                worksheet.write(i, 1, 'id')
                worksheet.write(i, 2, 'author')
                continue
            author_ = all[i - 1]['author']
            # 作者存在
            if author_:
                worksheet.write(i, 2, author_[0])
                worksheet.write(i, 0, all[i - 1]['title'])
                worksheet.write(i, 1, all[i - 1]['id'])
        workbook.close()
        print("生成Excel成功")
    except Exception as e:
        print('生成Excel失败：%s' % e)
    print('正在生成txt...')
    try:
        with open('%s/数组格式.txt' % save_path, "w") as f:
            f.write(str(all))
            print('生成txt成功')
    except Exception as e:
        print('生成txt失败：%s' % e)
print('共爬取%d篇文章' % a)
