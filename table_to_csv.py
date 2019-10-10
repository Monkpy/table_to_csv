# -*- coding: utf-8 -*-
import csv
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

# 解决表格问题---单位在上金额在下


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
}


def parse_table(url):
    req = urllib.request.Request(url=url, headers=headers)
    html = urlopen(req)
    bsObj = BeautifulSoup(html, "html.parser")  # bs4解析网页
    # table = bsObj.findAll('table', {'width': '579'})[0]  # 定位table 取第一个  url3
    # table = bsObj.findAll("table")[0]  # 定位table 取第一个 url url1 url2
    table = bsObj.findAll('table', {'class': 'MsoNormalTable'})  # url4
    if table:
        table = table[1]
        # print(table)  # 测试
        rows = table.findAll("tr")  # 定位table子节点
        csvFile = open("table_csv.csv", 'w', newline='', encoding='utf-8')  # 创建csv文件
        writer = csv.writer(csvFile)  # 写入内容
        money = ''
        try:
            # 循环子节点 tr
            for row in rows:
                csvRow = []  # 创建列表
                # 循环子节点tr 定位下一级节点
                for cell in row.findAll(['td']):
                    cell = cell.get_text().replace('\n', '').replace('\r', '').replace(' ', '')  # 获取网页表格数据
                    # 判定定位所需的值
                    if cell == '正式预算价(万元)':
                        money = str(cell)
                    elif cell == '发包价（万元）':
                        money = str(cell)
                    elif cell == '发包项目估算价(万元)':
                        money = str(cell)
                    # 将将表格数据添加到刚才创建的列表----几个tr就会创建几个列表---很有意思，不知道为什么。。。
                    csvRow.append(cell)
                # print(csvRow)
                writer.writerow(csvRow)  # 将列表写入csv文件
            # writer.writerow('/n')
            return money
        finally:
            # 关闭csv文件
            csvFile.close()
    else:
        money = ''
        return money


def get_money(url):
    money = parse_table(url)
    # print(money)
    if money != '':
        tb = pd.read_csv('table_csv.csv', usecols=[money], encoding='utf-8')  # 读取指定列 usecols=['',''] 必须等于一个列表
        lt = tb.iloc[:1]  # 读取指定行
        # print(tb)
        # print(lt)

        lt1 = lt.values[0]
        lt2 = str(lt1)
        ltz = lt2[1:-1]
        # print('------')
        # print(ltz)
        return ltz
    else:
        return money


# url = 'http://www.jxsggzy.cn/web/jyxx/002006/002006001/20190320/fa628bec-60ca-4d22-943f-d64916d00180.html'  # 测试网址--已成功
# url1 = 'http://www.jxsggzy.cn/web/jyxx/002006/002006001/20190514/3e43766d-ca11-4e4c-baad-382b3178043d.html'
# url2 = 'http://www.jxsggzy.cn/web/jyxx/002006/002006001/20190514/0f1ead8e-8654-4e71-ac0c-9107f50b31dc.html'  # 存在问题需要解决
# url3 = 'http://www.sdein.gov.cn/zwgk/gsgg/201906/t20190611_2263804.html'
url4 = 'http://218.90.220.218/xhweb/InfoDetail/?InfoID=2d7d6663-284c-4766-88d6-1102445f4d0a&CategoryNum=005001001'
# url5 = 'http://218.90.220.218/xhweb/InfoDetail/?InfoID=3a09e2ec-2103-4a7a-bfb6-14cec27ac6bf&CategoryNum=005001001'

amount = get_money(url4)
print(amount)


