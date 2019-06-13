# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BmwItem(scrapy.Item):
    # define the fields for your item here like:
    category = scrapy.Field()
    image_urls = scrapy.Field()  # 用来存储需要下载文件的连接，需要给一个列表
    images = scrapy.Field()



