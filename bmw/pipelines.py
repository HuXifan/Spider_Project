# -*- coding: utf-8 -*-

# Define your item pipelines here
# 存储到磁盘
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from urllib import request
from scrapy.pipelines.images import ImagesPipeline
from bmw import settings


class BmwPipeline(object):

    def __init__(self):
        # 判断 绝对路径W:\selfstudy\网络爬虫\hxf_11_scrapy\bmw
        self.path = os.path.dirname(os.path.dirname(__file__))  # 拿到bmw路径名称
        self.path = os.path.join(self.path, "images")  # 得到bmw/images路径名称
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
            image_name = url.split("_")[-1]  # 分割url下划线_后面的内容座位名字
            request.urlretrieve(url, os.path.join(category_path, image_name))

        return item


class BMWImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):  # 此方法在发送下载请求之前调用，本身就是发送下载请求的
        request_objs = super(
            BMWImagesPipeline,
            self).get_media_requests(
            item,
            info)  # 返回一个request对象列表
        # 遍历列表
        for request_obj in request_objs:
            request_obj.item = item
        return request_objs

    def file_path(self, request, response=None, info=None):
        # 此方法在图片将要被存储是调用
        path = super(
            BMWImagesPipeline,
            self).file_path(
            request,
            response,
            info)
        category = request.item.get('category')
        images_store = settings.IMAGES_STORE
        category_path = os.path.join(images_store, category)
        if not os.path.exists(category_path):
            os.mkdir(category_path)  # 如果不存在就创建分类目录
        image_name = path.replace("full/", "")  # 获取图片名字
        image_path = os.path.join(category_path, image_name)
        return image_path
