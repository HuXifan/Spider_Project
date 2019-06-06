# -*- coding: utf-8 -*-

# Define your item pipelines here
# 存储到磁盘
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from urllib import request
from scrapy.pipelines.images import ImagesPipeline


class BmwPipeline(object):

    def __init__(self):
        # 判断 绝对路径W:\selfstudy\网络爬虫\hxf_11_scrapy\bmw
        self.path = os.path.dirname(os.path.dirname(__file__))  # 拿到bmw路径名称
        self.path = os.path.join(self.path, "images")
        # print(images_path)
        # 判断images文件夹是否存在 如果没有就创建
        if not os.path.exists(self.path):
            # print("images文件夹不存在")
            os.mkdir(self.path)  # 创建images目录

    def process_item(self, item, spider):
        category = item['category']
        urls = item['urls']
        # 构建images下的分类category路径
        category_path = os.path.join(self.path, category)
        if not os.path.exists(category_path):
            os.mkdir(category_path)

        for url in urls:
            image_name = url.split("_")[-1]  # 分割url下划线后面的内容座位名字
            request.urlretrieve(url, os.path.join(category_path, image_name))

        return item


class BMWImagesPipeline(ImagesPipeline):
    pass

    def file_path(self, request, response=None, info=None):
        path = super(
            BMWImagesPipeline,
            self).file_path(
            request,
            response,
            info)
