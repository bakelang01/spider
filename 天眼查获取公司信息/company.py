# This Python file uses the following encoding: utf-8
# 作者：black_lang
# 创建时间：2022/5/17 18:49
# 文件名：company.py
import json

import time
import pandas as pd
import openpyxl as ex
from lxml import etree
import requests

def get_csv(path):
    print('读取csv文件')
    table = pd.read_csv(path)
    le = table.shape[0]
    com_li=[]
    for i in range(le):
        com=[]
        com.append(table.loc[i][0])
        com.append(table.loc[i][1])
        com_li.append(com)
    return com_li


# 获得源码信息
def get_html(name):
    global FAIL
    print('开始解析数据')
    url = name[1]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
    }
    ch_f =0
    while True:

       try:
            response = requests.get(url=url,headers=headers)
            if response.status_code == 200:
                response.encoding='utf-8'
                tree = etree.HTML(response.text)
                di={}

                di['title'] = tree.xpath('//*[@id="company_web_top"]/div[3]/div[3]/div[1]/span/span/h1/text()')[0]

                place = tree.xpath('//*[@id="company_web_top"]/div[3]/div[3]/div[3]/div[3]/div[2]/span/div/div/div/text()')[0].replace('&nbsp','').replace('\xa0','')
                if '市' in place:
                    place=place.split('市')[0]+'市'
                elif '区' in place:
                    place = place.split('区')[0]+'区'
                di['place'] = place

                di['new']  = tree.xpath('//*[@id="company_web_top"]/div[3]/div[3]/div[3]/div[4]/div/div/text()')[1].replace('\xa0','')
                di['date'] = tree.xpath('//*[@id="_container_baseInfo"]/table/tbody/tr[2]/td[2]/text()')[0]
                tr_li = tree.xpath('//table[@class="table -rongzi -sort"]/tbody/tr')
                tds=[]
                for tr in tr_li:
                    td=[]
                    td.append(tr.xpath('./td[2]/text()')[0]) # 时间
                    td.append(tr.xpath('./td[3]/text()')[0]) # 金额
                    td.append(tr.xpath('./td[4]/div[1]/text()')[0]) #伦次
                    td.append('、'.join(tr.xpath('./td[7]//text()')))
                    tds.append(td)
                di['rongzi'] = tds
                print(di['title'],'解析成功!')
                return di
            else:
                print('响应错误',response.status_code)
       except:
            ch_f+=1
            print(f'第{ch_f}次重新获取数据')
            if ch_f == 5:
                FAIL.append(name)
                print(name)
                return {}


#分析数据
def save_data(data):
    print('开始保存数据！')
    wb = ex.load_workbook('2_information.xlsx')
    sheet = wb.active
    for di in data:
        wr = []
        wr.append(di['title'])
        wr.append(di['place'])
        wr.append(di['date'])
        wr.append(di['new'])
        if di['rongzi'] != []:
            wr.extend(di['rongzi'][0]) # 融资最新消息
            t=''
            for rong in di['rongzi']:
                t += rong[3]
            wr.append(t) # 历史融资
        else:
            print(di['title'],di['rongzi'],'未获得融资信息','!'*50)
        sheet.append(wr)
    wb.save('2_information.xlsx')
    print('保存数据成功！','+'*10)

if __name__ =='__main__':
    N=0
    FAIL=[]
    file = 'hrefs.csv'
    com_li = get_csv(file)
    # com_li = [['中国赛宝实验室', 'https://www.tianyancha.com/company/1137931099'], ['阿里巴巴集团控股有限公司', 'https://www.tianyancha.com/company/80351256'],['索信达控股有限公司', 'https://www.tianyancha.com/company/3395191448'],['上海自动化仪表股份有限公司', 'https://www.tianyancha.com/company/3079798342'],['亚信科技控股有限公司', 'https://www.tianyancha.com/company/3395075518']]
    count = 0
    data = []
    for name in com_li:
        N += 1
        print('信息数>>', N, )
        infor = get_html(name)
        if not bool(infor):
            continue
        count += 1
        data.append(infor)
        if count == 20:
            save_data(data)
            count = 0
            data = []
    save_data(data)
    print('获取信息失败>>\n',FAIL)

# [['中国赛宝实验室', 'https://www.tianyancha.com/company/1137931099'], ['阿里巴巴集团控股有限公司', 'https://www.tianyancha.com/company/80351256'],['索信达控股有限公司', 'https://www.tianyancha.com/company/3395191448'],['上海自动化仪表股份有限公司', 'https://www.tianyancha.com/company/3079798342'],['亚信科技控股有限公司', 'https://www.tianyancha.com/company/3395075518']]




