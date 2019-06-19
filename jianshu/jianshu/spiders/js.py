# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianshu.items import ArticleItem


class JsSpider(CrawlSpider):
    name = 'js'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    rules = (
        # .* 可有可无  follow=True
        Rule(
            LinkExtractor(
                allow=r'.*/p/[0-9a-z]{12}.*'),
            callback='parse_detail',
            follow=True),
    )  # rules 元组 必须有逗号,

    def parse_detail(self, response):
        # 实现网页的解析

        title = response.xpath("//h1[@class='title']/text()").get()
        # 依然 scrapy shell验证
        author = response.xpath(
            "//div[@class='info']//span[@class='name']/a/text()").get()
        avatar = response.xpath(
            "//div[@class='author']//a[@class='avatar']/img/@src").get()
        # //upload.jianshu.io/users/upload_avatars/10955200/06d18db0-0bc4-494c-b9a7-f541525c9e80.jpg?imageMogr2/auto-orient/strip|imageView2/1/w/96/h/96
        # url不完整
        pub_time = response.xpath(
            "//span[@class='publish-time']/text()").get().replace("*", "")
        # url1 https://www.jianshu.com/p/f85a78b5f1bf?utm_campaign=maleskine&utm_content=note&utm_medium=seo_notes&utm_source=recommendation
        # url2 https://www.jianshu.com/p/6bd0bd54ab02
        # 两种url 第一种只出现一个？
        url = response.url
        url1 = url.split("?")[0]
        # url1 = ['https://www.jianshu.com/p/f85a78b5f1bf', 'utm_campaign=maleskine&utm source=recommendation']
        article_id = url1.split("/")[-1]
        origin_url = response.url
        # content = response.xpath("//div[@class='show-content']//p//text()").getall()
        content = response.xpath("//div[@class='show-content']").get()

        # ajax+selenium
        word_count = response.xpath("//span[@class='wordage']/text()").get()
        read_count = response.xpath("//span[@class='views-count']/text()").get()
        like_count = response.xpath("//span[@class='likes-count']/text()").get()
        comment_count = response.xpath("//span[@class='comments-count']/text()").get()

        subjects = response.xpath("//div[@class='include-collection']//a/div/text()").getall()  # 获取所有主题 返回一个列表
        subjects = ','.join(subjects)  # 变成字符串
        # mysql  不支持存储列表

        item = ArticleItem(title=title,
                           author=author,
                           avatar=avatar,
                           article_id=article_id,
                           origin_url=origin_url,
                           pub_time=pub_time,
                           content=content,

                           word_count=word_count,
                           read_count=read_count,
                           comment_count=comment_count,
                           like_count=like_count,
                           subjects=subjects
                           )
        yield item
        # 代码最后使用yield关键字提交item，讲此方法打造成一个生成器，是parse（）方法中最精彩的地方

