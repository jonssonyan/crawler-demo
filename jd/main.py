# !/usr/bin/python
# -*- coding: UTF-8 -*-
# import时导入内置的或者第三方的包
import json

import requests
import xlsxwriter


# 移除字符串前缀，参数解释：string指需要截取的字符串，prefix指需要匹配并移除的字符串
def remove_prefix(string, prefix):
    if not (isinstance(string, str) and isinstance(prefix, str)):
        raise TypeError('Param value type error')
    if string.startswith(prefix):
        return string[len(prefix):]
    return string


# 移除字符串后缀
def remove_suffix(string, suffix):
    if not (isinstance(string, str) and isinstance(suffix, str)):
        raise TypeError('Param value type error')
    if string.endswith(suffix):
        return string[:-len(suffix)]
    return string


# 请求时加上请求头，防止服务器发现是爬虫的请求
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'Host': 'club.jd.com',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive'
}
# 要请求的url地址
url = 'https://club.jd.com/comment/productPageComments.action'
# 存储爬取的数据
data_arr = []
# 评价的评价分类的枚举
score_map = {7: '视频晒单', 5: '追评', 4: '晒图', 3: '好评', 2: '中评', 1: '差评', 0: '全部评价'}
# 评价的评分
score_ = -1
# 主函数，程序的入口
if __name__ == '__main__':
    # 获得用户的一些输入
    product_id = input('请输入商品id：') or '2943079'
    score = input('请输入评价类型（0：全部评价; 1：差评; 2：中评; 3：好评; 4：晒图; 5：追评; 7：视频晒单）：') or '0'
    page_num = input('请输入爬取页数：') or '10'

    print("开始爬取...")
    # 循环请求
    for i in range(1, int(page_num) + 1):
        # try catche是用来捕获异常
        try:
            # 实际的请求，用的request第三方包，参数解释，url：请求的地址，请求的参数：（page：页号，pageSize：页大小，callback：返回json格式，productId：商品id，score：评价类型）
            # timeout超时时间，如果请求5ms内没有相应就是超时
            response = requests.get(url=url, headers=headers,
                                    params={'page': i,
                                            'pageSize': 10,
                                            'callback': 'fetchJSON_comment98',
                                            'productId': product_id,
                                            'score': score,
                                            'sortType': 5},
                                    timeout=5)
        except requests.exceptions.RequestException as e:
            print("请求异常：%s", e)
            break
        print("正在爬取第%d页" % i)
        # 解析请求后返回的参数
        text = response.text
        text = remove_prefix(text, 'fetchJSON_comment98(')
        text = remove_suffix(text, ');')
        loads = json.loads(text)
        score_ = loads['score']
        # 把爬取到的评论信息保存到到data_arr
        data_arr.extend(loads['comments'])
    print("爬取结束...")
    try:
        # 如果存储数据的data_arr对象内容不是空就将数据导出到excel中
        if len(data_arr) > 0:
            print('正在生成Excel...')
            # excel的名称
            workbook = xlsxwriter.Workbook('./京东生鲜在线评论.xlsx')
            # 添加一个sheet页，我们只需要一个sheet页存储数据就够了
            worksheet = workbook.add_worksheet()
            for i in range(0, len(data_arr) + 1):
                # 第一行用于写入表头
                if i == 0:
                    worksheet.write(i, 0, '网址')
                    worksheet.write(i, 1, '商品名称')
                    worksheet.write(i, 2, '标题')
                    worksheet.write(i, 3, '评价星级')
                    worksheet.write(i, 4, '评价类型')
                    worksheet.write(i, 5, '评价用户')
                    worksheet.write(i, 6, '评价内容')
                    worksheet.write(i, 7, '评价时间')
                    continue
                # 第二行之后就开始写如怕渠道的数据
                # url
                worksheet.write(i, 0, 'https://item.jd.com/%s.html' % product_id)
                worksheet.write(i, 1, data_arr[i - 1]['productColor'])
                worksheet.write(i, 2, data_arr[i - 1]['referenceName'])
                # 评分
                worksheet.write(i, 3, data_arr[i - 1]['score'])
                worksheet.write(i, 4, score_map.get(score_))
                # 昵称
                worksheet.write(i, 5, data_arr[i - 1]['nickname'])
                # 内容
                worksheet.write(i, 6, data_arr[i - 1]['content'])
                # 内容时间
                worksheet.write(i, 7, data_arr[i - 1]['creationTime'])
            # 关闭资源，申请过的资源记得关闭
            workbook.close()
            print("生成Excel成功")
            print('正在生成txt...')
            for i in range(0, len(data_arr) + 1):
                try:
                    with open('./京东生鲜在线评论.txt', "a") as f:
                        f.write('%s\n' % data_arr[i - 1]['content'])
                except Exception as e:
                    print('生成txt失败：%s' % e)
            print('生成txt成功')
    except IOError:
        print("生成Excel异常...")
