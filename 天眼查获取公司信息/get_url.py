# This Python file uses the following encoding: utf-8
# 作者：black_lang
# 创建时间：2022/5/17 23:56
# 文件名：get_url.py
import time

import openpyxl as py
import requests
from lxml import etree
import re

def get_excel(path):
    com_li=[]
    wb = py.load_workbook(path)
    sheet = wb.active
    for cell in sheet['A']:
        com_li.append(cell.value)
    return com_li

def res(key):
    url = f'https://www.tianyancha.com/search?key={key}'
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    }
    data = requests.get(url=url,headers=headers)
    data.encoding='utf-8'
    tree = etree.HTML(data.text)
    try:
        href = 'https://www.tianyancha.com/company/'+tree.xpath('//*[@id="search_company_0"]/div/@data-id')[0]
    except:

        href = ' '
    return href


"""
传入一份全是公司全名称的表格，然后先会爬取每一个公司的详情页的url 并保存在一个csv文件中，再有由另一个程序代码进行信息的获取存储
之所以没有合并两个py文件，是因为懒
如果想要公司其他信息，也可以解析其他对应信息
"""

filepath = 'commpanys.xlsx'
com_li = get_excel(filepath)
with open('hrefs_1.csv','w',encoding='utf-8') as f:
    count = 1
    for name in com_li:
        print(count, '>>')
        count+=1
        num = 0
        while True:
            href = res(name)
            print(name,href)
            num+=1
            if href != ' ' or num == 5:
                break
        num = 0
        f.write(name+','+href+'\n')

