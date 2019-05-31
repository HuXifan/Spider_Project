# -*- coding: utf-8 -*-
import scrapy
from yangguang.items import YangguangItem

class YgSpider(scrapy.Spider):
    name = 'yg'
    allowed_domains = ['sun0769.com']
    start_urls = ['http://wz.sun0769.com/index.php/question/questionType?type=4&page=0']

    def parse(self, response):
        # 分组
        pass
        tr_list = response.xpath("//div[@class='greyframe']/table[2]/tr/td/table/tr")
        for tr in tr_list:
            item = YangguangItem()  # 实例化
            item["title"] = tr.xpath("./td[2]/a[@class='news14']/@title").extract_first()
            item["href"] = tr.xpath("./td[2]/a[@class='news14']/@href").extract_first()
            item["pub_date"] = tr.xpath("./td[last()]/text()").extract_first()

            yield scrapy.Request(
                item["href"],
                callback=self.parse_detail,
                meta={"item": item}
                # meta 是一个字典,帮助实现数据在parse和parse_detail之间传递

            )
        # 翻页
        # next_url 通过文本定位
        next_url = response.xpath("//a[text()='>']/@href").extract_first()
        # 判断是否有None值是否有下一页
        if next_url is not None:
            # 构造下一页请求
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )

    def parse_detail(self, response):  # 处理详情页
        item = response.meta["item"]  # 取meta里的item
        item["content"] = response.xpath("//div[@class='wzy1']/table[2]/tr[1]/td[@class='txt16_3']//text()").extract()  # 多段文字
        item["content_img"] = response.xpath("//div[@class='wzy1']/table[2]/tr/td[@class='txt16_3']//img/@src").extract()  # 可能多张文字
        item["content_img"] = ["http://wz.sun0769.com"+i for i in item["content_img"]]
        yield item  # 传给pipeline



















