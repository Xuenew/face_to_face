# 若能避开猛烈的欢喜,自然也不会有悲痛的来袭,
# 迎着风雨走 孤独且自由,
# Author: xyy, time:2020/2/17
import asyncio
import time

from selenium import webdriver
from pyppeteer import launch
from lxml import etree

class Selenium_Pyppeteer():

    # 不管那个方式 每个页面返回所有的图片连接和当前页面URL
    # 不管那种 预留反爬虫的空闲

    def __init__(self,get_url:str):
        self.get_url = get_url
    def get_drver(self):
        # options = webdriver.ChromeOptions()
        #
        # # 设置图片不显示
        # prefs = {"profile.managed_default_content_settings.images":2}
        # options.add_experimental_option("prefs",prefs)
        # #options.add_argument('--headless')
        # driver = webdriver.Chrome(chrome_options=options)
        driver = webdriver.Chrome()

        #设置页面打开超时 时间， 15s
        driver.set_page_load_timeout(15)
        return driver
    def selenium_get(self)->"list of img":
        driver = self.get_drver()
        # print("xxxxx")
        driver.get(self.get_url)
        html = driver.page_source
        #driver.execute_script("alert('执行了js selenium')")
        driver.close()
        return html

    def pyppeteer_get(self)->"list of img":

        return asyncio.run(self.pyppeteer_Get())
        # return asyncio.get_event_loop().run_until_complete(self.pyppeteer_Get())

    # 异步调用
    async def pyppeteer_Get(self)->"list of img":
        browser = await launch(headless = False)   # headless = False，默认ture，为无头模式
        # browser = await launch(headless = True)   # headless = False，默认ture，为无头模式
        page = await browser.newPage()


        await page.goto(self.get_url)
        # await page.screenshot({'path': 'example.png'}) # 热点图


        html = await page.content()
        await page.close()
        return html
if __name__ == '__main__':
    p = Selenium_Pyppeteer(get_url="https://www.aliexpress.com/item/32858244065.html")
    # p = Selenium_Pyppeteer()
    p.pyppeteer_get()




    # p.get_url = "http://www.xueyiyang.top"
    # p.selenium_get()
    # asyncio.run(p.pyppeteer_Get())