#-- coding=utf-8 --
# 导入模块
import requests
from lxml import etree
import pymysql

def connectSQL(USER,PASSWORD):
    # 链接到数据库
    SQ = pymysql.connect(user=USER, password=PASSWORD, host='localhost')
    cur = SQ.cursor()
    try:  # 已经存在数据表，就进行报错捕获
        # 创建一个数据库,数据库表
        tbname = 'stock'
        cur.execute("""CREATE DATABASE """+tbname)
        SQL1 = pymysql.connect(
            user=USER,
            password=PASSWORD,
            database=tbname,
            host='localhost'
        )
        cur1 = SQL1.cursor()
        # 创建索引 id,commpany,title,source,date,href
        create_table = """
        CREATE TABLE test (
                id char(10),
                company VARCHAR(50),
                title VARCHAR(250) ,
                source VARCHAR(250),
                date VARCHAR(100),
                href VARCHAR(250)
        )"""
        # 创建表格
        cur1.execute(create_table)
        # 关闭链接
        SQL1.close()
        # 提示
        print("表格创建完成！\n")
    except:
        # 表格存在，跳过
        print("已有数据表格。\n")
        # 关闭链接
        SQ.close()

def write_data(USER,PASSWORD,infors):
    '''
    存储数据
    '''
    count=1
    SQL3=pymysql.connect(host='localhost',user=USER,password=PASSWORD,database='stock')
    # 将每一行都存储到数据库中
    for n in infors:
        if n:
            cur3 = SQL3.cursor()
            try:
                # 进行数据插入
                cur3.execute(
                    '''INSERT INTO test(id,company,title,source,date,href) VALUES ("%s","%s","%s","%s","%s","%s")''',
                    (
                        str(count),
                        n[4],
                        n[0],
                        n[1],
                        n[2],
                        n[3]
                    )
                )
                SQL3.commit()
                # 索引加1
                print(f"第{count}条成功写入")
                count=count+1
            except:
                # 若插入失败，给出提示
                print("信息写入失败！")
        else:
            continue
    print("数据写入成功！")
    # 关闭数据库链接
    SQL3.close()



def get_data(URL,start,end):
    code = URL.rsplit(',')[1].rsplit('_')[0]
    # print(code)
    urls=[f'http://guba.eastmoney.com/list,{code}_%d.html' % i for i in range(start,end)] # 网址列表
    # 请求头的伪装
    headers={
        # 'Host': 'guba.eastmoney.com',
        'Referer': f'http://guba.eastmoney.com/list,{code}_2.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/97.0.4692.99 Safari/537.36& '
    }
    #  信息存储列表
    infos=[]
    # 批量获取数据
    for url in urls:
        html = requests.get(url=url,headers=headers).text # 发送请求
        et=etree.HTML(html)  # 进行数据解析
        divs=et.xpath('//div[@id="mainbody"]/div[4]/div') # 获取部分
        name = et.xpath('//*[@id="stockname"]/a/text()')[0].replace('股', '').replace('吧', '')
        for div in divs: # 得到每一条关于股票的信息
            # 创建临时的存储一条信息的列表
            news = []
            try:
                # 对数据进行解析获得股票的title
                ti = div.xpath('./span[@class="l3 a3"]/a/@title')[0]
                # 把title存储到列表中
                news.append(ti)
                # 对数据进行解析获得股票的score
                sc = div.xpath('./span[@class="l4 a4"]/a/font/text()')[0]
                # 把score存储到列表中
                news.append(sc)
                # 对数据进行解析获得股票的date
                da = div.xpath('./span[@class="l5 a5"]/text()')[0]
                # 把date存储到列表中
                news.append(da)
                # 对数据进行解析获得股票的href
                hr = div.xpath('./span[@class="l3 a3"]/a/@href')[0]
                # 把href存储到列表中
                news.append(hr)

                # 把name存储到列表中
                news.append(name)
            except:
                pass # 异常处理
            infos.append(news)
    # 提示信息
    print("数据获取成功！")
    return infos


if __name__ == '__main__':
    # 全局变量，数据库用户信息
    USER = 'root'
    PASSWORD = '1112'

    # 东方财富网股吧的网址
    URL = 'http://guba.eastmoney.com/list,000725_02.html' # 随便一页的url，因为只是为了解析出code 000725这个

    #创建数据库里的表格
    connectSQL(USER,PASSWORD)

    # 获取数据
    infos = get_data(URL,start=1,end=5)
    # print(infos)

    # 写入数据
    write_data(USER,PASSWORD,infos)





