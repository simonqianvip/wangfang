# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WangfangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    """
     title = selector.xpath('/html/body/div[3]/div/h1/text()').extract()
        summary = selector.xpath('/html/body/div[3]/div/div[2]/div/div[2]/text()').extract()
        author = selector.xpath('/html/body/div[4]/div/div[2]/span[2]/a/text()').extract()
        # 作者单位
        author_unit = selector.xpath('/html/body/div[4]/div/div[3]/span[2]/text()').extract()
        # 刊名
        article_name = selector.xpath('/html/body/div[4]/div/div[4]/span[2]/a/text()').extract()
        article_name_1 = selector.xpath('/html/body/div[4]/div/div[4]/span[2]/span/span[1]/@title').extract()
        article_name_2 = selector.xpath('/html/body/div[4]/div/div[4]/span[2]/span/span[2]/@title').extract()
        # 年卷
        year = selector.xpath('/html/body/div[4]/div/div[6]/span[2]/a/text()').extract()
        # 分类
        classification = selector.xpath('/html/body/div[4]/div/div[7]/span[2]/text()').extract()
        # 关键词
        keywords = selector.xpath('/html/body/div[4]/div/div[8]/span[2]/a/text()').extract()
        # 机标分类号
        standard = selector.xpath('/html/body/div[4]/div/div[9]/span[2]/text()').extract()
        # 出版日期
        publish = selector.xpath('/html/body/div[4]/div/div[10]/span[2]/text()').extract()
    """
    # 标题
    title = scrapy.Field()
    # 摘要
    summary = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 作者单位
    author_unit = scrapy.Field()
    # 刊名
    article_name = scrapy.Field()
    # 年卷
    years = scrapy.Field()
    # 分类
    classification = scrapy.Field()
    # 关键词
    keywords = scrapy.Field()
    # 机标分类号
    standard = scrapy.Field()
    # 出版日期
    publish = scrapy.Field()
    # 引用
    # reference = scrapy.Field()
    # 被引用
    # referenced = scrapy.Field()
    # content = Field()
    pass
