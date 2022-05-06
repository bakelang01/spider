# --code=utf-8--
import requests
from lxml import etree

def get_html(url):
    next_url=url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
    }
    totle_page = 0
    while True:
        receives = []
        response = requests.get(url=next_url, headers=headers)
        response.encoding = 'utf-8'
        tree = etree.HTML(response.text)
        try:
            global FILE_RECEIVE
            FILE_RECEIVE = tree.xpath('//div[@id="content"]/h1/text()')[0]
            num_page = tree.xpath('//div[@id="content"]//div[@class="paginator"]/span[@class="thispage"]/text()')[0]
            if totle_page == 0:
                totle_page = tree.xpath('//*[@id="content"]//div[@class="paginator"]/span[2]/@data-total-page')[0]
            print(FILE_RECEIVE, f'正在获取数据： {num_page}/{totle_page}', '+' * 50)
            div_list = tree.xpath('//div[@class="review-list  "]/div')
            for div in div_list:
                re_dir = {}
                re_dir["id"] = div.xpath('./div/header/a[@class="name"]/text()')[0]
                try:
                    re_dir["level"] = div.xpath('./div/header[@class="main-hd"]/span[1]/@title')[0]
                    re_dir["date"] = div.xpath('./div/header[@class="main-hd"]/span[2]/text()')[0]
                except:
                    re_dir["level"] = None
                    re_dir["date"] = div.xpath('./div/header[@class="main-hd"]/span[1]/text()')[0]
                re_dir["page"] = div.xpath('./div//div[@class="main-bd"]/h2/a/text()')[0]
                re_dir["href"] = div.xpath('./div/div[@class="main-bd"]/h2/a/@href')[0]
                re_dir["useful_count"] = div.xpath('./div//div[@class="action"]/a[1]/span/text()')[0].replace(' ',
                                                                                                              '').replace(
                    '\n', '')
                re_dir["no_useful_count"] = div.xpath('./div//div[@class="action"]/a[2]/span/text()')[0].replace(' ',
                                                                                                                 '').replace(
                    '\n', '')
                re_dir["return"] = div.xpath('./div//div[@class="action"]/a[3]/text()')[0]
                receives.append(re_dir)
        except:
            pass

        try:
            next_page=tree.xpath('//span[@class="next"]/a/@href')[0]
            if '?start=' in url:
                print(url)
                url=url.split('?start=')[0]
            next_url=url+next_page
        except:
            break
        down_data(receives)


def down_data(receives):
    global FILE_RECEIVE
    global COUNT_PL
    filename=FILE_RECEIVE+'.txt'
    with open(filename,'a+',encoding='utf-8') as f:
        for receive in receives:
            f.write(str(receive)+'\n')
            COUNT_PL+=1
            if MAX_COUNT >= 0:
                if COUNT_PL >= MAX_COUNT:
                    print("已获取到指定数量的评论！", '=' * 80)
                    exit(0)
    print("存储完成！",'='*80)


#  豆瓣影评：传入一个影评界面的url，将会自动爬取该电影的所有评论信息，并以字典形式每一行为一条影评信息保存在txt文件中

#  优化方向：
#     1.完善url的传入，可以找到一个豆瓣接口，输入电影名称，就会自动生成其对应的url
#     2.可以用tkinter制作一个简单的GUI，实现界面化操作
#     3.对得到的影评信息进行可视化操作，从数据中获得价值，比如生成影评词云等
#     4.代码自身也可优化，有些地方过于冗余，可改进使其更加优雅（其实就是自己懒）
#     5.代码有几处报错，直接用try模糊处理了过去，并没有深究其原因，可改进

if __name__ == '__main__':
    FILE_RECEIVE = None # 保存的文件名
    MAX_COUNT = -1
    COUNT_PL = 0 # 记录获取的评论提示数量

    while True:
        chose = input('是否设置最大评论数获取量 (n/y) :')
        if chose == 'y':
            MAX_COUNT = int(input('输入获取评论数量： '))
            break
        elif chose == 'n':
            break
            pass
        else:
            print('选择错误！重新选择')
    url=input("豆瓣评论网址(比如 https://movie.douban.com/subject/26752088/reviews)\n>>> ")
    get_html(url)
