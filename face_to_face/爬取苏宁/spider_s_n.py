# 若能避开猛烈的欢喜,自然也不会有悲痛的来袭,
# 迎着风雨走 孤独且自由,
# Author: xyy, time:2020/3/17

import requests
import re
from lxml import etree

from Base_Rmq_Object import Base_Mq
from sn_selenium_pyppteer_getimg import Selenium_Pyppeteer
from save_to_mysql_sn import get_info_from_mysql

btm = Base_Mq("su_ning")

class spider_sn():

    def __init__(self,art_id="",g_start_url = ""):
        self.art_id = art_id
        self.start_url = g_start_url

    def start_pypuetter_page(self): # 启动 浏览器
        pyppuetter_page = Selenium_Pyppeteer(get_url=self.start_url)
        return pyppuetter_page.pyppeteer_get

    def start_selenium_driver(self):
        selenium_driver = Selenium_Pyppeteer(get_url=self.start_url)
        return selenium_driver.selenium_get()


    def sample_get(self):
        res = requests.get(url=self.start_url)
        return res.text

    def get_price(self,goods_id):
        url = "https://ds.suning.com/ds/generalForTile/0000000{}_____-010-2-0000000000-1--ds0000000008417.jsonp?callback=ds0000000008417".format(goods_id)

        payload = {}
        headers= {}
        
        response = requests.request("GET", url, headers=headers, data = payload)
        
        # print(response.text)
        info = response.text
        false = False
        true = True
        none = None
        null = None
        res_re_data = re.findall(r"ds0000000008417\((.*?)\);",info)
        # print(res_re_data)
        res_re_data = eval(res_re_data[0]) if res_re_data else {}
        if res_re_data:
            # print(len(res_re_data))
            # print(type(eval(res_re_data[0])))
            return res_re_data["rs"][0]["price"]
        else:
            print("此商品未取到价格 商品ID 为{}".format(goods_id))
            # 错误的ID 放到队列里 再分析问题
            btm.save_mq(url=str(goods_id))
            return ""

    def anasies(self,html):
        selec = etree.HTML(html)
        item_list = selec.xpath("//div[@class='res-info']")
        # print("zong gong {}".format(len(item_list)))

        for each in item_list:
            title = "".join(each.xpath(".//div[@class='title-selling-point']//text()"))
            price_id = "".join(each.xpath(".//div[@class='price-box']//span/@datasku")).split("|")[0]
            # print(price,"是否是它的商品id")
            price = self.get_price(goods_id=price_id)
            assess = "".join(each.xpath(".//div[@class='evaluate-old clearfix']//text()"))
            print(title,price,assess)
            get_info_from_mysql(title,price,assess)


    def run(self):
        #driver = self.start_selenium_driver()
        html = self.sample_get()
        self.anasies(html)
       


if __name__ == '__main__':
    # 测试版
    # p = spider_sn(g_start_url='https://list.suning.com/0-243505-0.html?safp=d488778a.homepage1.99345513004.84&safc=cate.0.0')
    # p.run()

    # 运行
    for num in range(0,5):
        print("当前执行到 --->>> page {}".format(num))
        p = spider_sn(g_start_url="https://list.suning.com/emall/searchV1Product.do?ci=243505&pg=03&cp=0&il=0&iy=0&isNoResult=0&n=1&sesab=&id=IDENTIFYING&cc=010&paging={}&sub=0&jzq=7896".format(num))
        p.run()

    # p.get_price(goods_id=10546607020)