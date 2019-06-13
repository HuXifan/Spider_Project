# -*- coding: utf-8 -*-
import scrapy
from bmw.items import BmwItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class Bmw5Spider(CrawlSpider):
    name = 'bmw5'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = [
        'https://car.autohome.com.cn/pic/series/202.html']

    rules = (
        Rule(
            LinkExtractor(
                allow=r"https://car.autohome.com.cn/pic/series/202-.+"),
            callback="parse_page",
            follow=True),
        # follow=True 如果有下一页 跟进
    )

    def parse_page(self, response):
        category = response.xpath(
            "//div[@class='uibox']//div[@class='uibox-title']/text()").get()  # 拿到分类
        # contains函数 包含属性
        srcs = response.xpath(
            "//div[contains(@class,'uibox-con')]/ul/li//img/@src").getall()
        # src //car2.autoimg.cn/cardfs/product/g22/M04/97/CB/t_autohomecar__wKgFW1kAR2eAMHttAAGErg6yXXs654.jpg
        srcs = list(map(lambda x: x.replace("t_", ""), srcs))  # 去掉t_
        # urls = []
        # for src in srcs:
        # urljoin(base, url, allow_fragments=True)  将基地址与一个相对地址形成一个绝对地址
        #     url = response.urljoin(src)
        #     urls.append(url)
        # src = https://car3.autoimg.cn/cardfs/product/g14/M12/7A/48/autohomecar__wKgH1VkAR2eAaQgZAAE6laymMxE167.jpg
        # srcs = list(map(lambda x: response.urljoin(x.replace("t_", "")),
        # srcs))  # 合并来写
        srcs = list(map(lambda x: response.urljoin(x), srcs))
        yield BmwItem(category=category, image_urls=srcs)

    def test_parse(self, response):  # 取消使用
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
            # map对象,用list()转化成列表
            urls = list(map(lambda url: response.urljoin(url), urls))

            item = BmwItem(category=category, image_urls=urls)
            yield item
