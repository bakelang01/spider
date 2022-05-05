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
            move_name = tree.xpath('//div[@id="content"]/h1/text()')[0]
            num_page = tree.xpath('//div[@id="content"]//div[@class="paginator"]/span[@class="thispage"]/text()')[0]
            if totle_page == 0:
                totle_page = tree.xpath('//*[@id="content"]//div[@class="paginator"]/span[2]/@data-total-page')[0]
            print(move_name, f'正在获取数据： {num_page}/{totle_page}', '+' * 50)
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
    global count_pinglun
    with open('豆瓣数据.txt','a+',encoding='utf-8') as f:
        for receive in receives:
            f.write(str(receive)+'\n')
            count_pinglun+=1
    print("存储完成！",'='*80)






if __name__ == '__main__':
    url='https://movie.douban.com/subject/1292052/reviews'
    count_pinglun=0
    get_html(url)
