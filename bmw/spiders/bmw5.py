# -*- coding: utf-8 -*-
import scrapy
from bmw.items import BmwItem

class Bmw5Spider(scrapy.Spider):
    name = 'bmw5'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = [
        'https://car.autohome.com.cn/pic/series/202.html#pvareaid=3454438']

    def parse(self, response):
        # selectorlist
        uiboxs = response.xpath("//div[@class='uibox']")[1:]  # 切片操作 过滤第一个
        #
        for uibox in uiboxs:
            category = uibox.xpath(
                ".//div[@class='uibox-title']/a/text()").get()  # 取到一份
            urls = uibox.xpath(".//ul/li/a/img/@src").getall()
            # for url in urls:
            #     # url = "https:" + url  # 所有图片连接
            #     url = response.urljoin(url)
            #     # print(url)
            urls = list(map(lambda url: response.urljoin(url), urls))  # map对象,用list()转化成列表

            item = BmwItem(category=category, image_urls=urls)
            yield item



