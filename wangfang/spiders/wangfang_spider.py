# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import scrapy.cmdline
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from wangfang.items import WangfangItem
import subprocess
import os,urllib2,urllib
import logging

from wangfang.mydownloader import MyDownloader


base_url = 'http://s.wanfangdata.com.cn/Paper.aspx'
download_pre = 'http://f.wanfangdata.com.cn/'

localDir = 'd:\\FireFox_Download\\'

logger = logging.getLogger(__name__)

class WangFangSpider(scrapy.Spider):
    # def __init__(self):
    #     # 实例化一个火狐配置对象
    #     pf = webdriver.FirefoxProfile()
    #     # 设置成0代表下载到浏览器默认下载路径；设置成2则可以保存到指定目录
    #     pf.set_preference("browser.download.folderList", 2)
    #     # 设置下载路径
    #     pf.set_preference("browser.download.dir", "d:\\FireFox_Download")
    #     pf.set_preference("browser.startup.homepage","about:blank")
    #     pf.set_preference("startup.homepage_welcome_url","about:blank")
    #     pf.set_preference("startup.homepage_welcome_url.additional","about:blank")
    #     # 不询问下载路径；后面的参数为要下载页面的Content-type的值 application/octet-stream
    #     pf.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream;application/pdf")
    #     # pf.set_preference("prefs.converted-to-utf8", "true")
    #     self.driver = webdriver.Firefox(firefox_profile=pf,
    #                                     executable_path = 'D:\Program Files\Mozilla Firefox\geckodriver-v0.10.0-win64\geckodriver.exe')
    #     self.driver.set_page_load_timeout(10)
        # options = webdriver.ChromeOptions()
        # options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
        # self.driver = webdriver.Chrome(chrome_options=options,executable_path='D:\program\chromedriver_win32\chromedriver.exe')

    name = "wf"
    allowed_domains = ["wanfangdata.com.cn"]
    start_urls = [
        'http://s.wanfangdata.com.cn/Paper.aspx?q=%E8%80%90%E7%81%AB'
    ]

    def parse(self, response):
        """
        1,获取列表页，每个论文的url
        2,获取下一页的url
        :param response:
        :return:
        """
        selector = Selector(response)
        links = selector.xpath('/html/body/div[2]/div[2]/div[2]/div/div[1]/div[1]/a[2]/@href').extract()
        for link in links:
            # print(link)
            yield scrapy.Request(link, callback=self.parse_content)

        page_links = selector.xpath('/html/body/div[2]/div[2]/div[2]/p/a/@href').extract()
        length = page_links.__len__()
        next_page_suffix = page_links[length - 1]
        # print(next_page_suffix)
        next_page_url = base_url + next_page_suffix

        if page_links[length - 1]:
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_content(self, response):
        selector = Selector(response)
        # self.driver.get(response.url)
        # WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/a[1]/i'))
        # self.driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/a[1]/i').click()

        logger.info('--------------------解析文章内容------------------------')

        div = selector.xpath('/html/body/div[4]/div/div').extract()
        # 获取文章标题
        title = selector.xpath('/html/body/div[3]/div/h1/text()').extract()
        # 获取文章摘要
        summary = selector.xpath('/html/body/div[3]/div/div[2]/div/div[2]/text()').extract()

        author = []
        author_unit = []
        article_name = []
        article_name_1 = []
        article_name_2 = []
        standard = ''
        classification = ''
        years = ''
        keywords = ''
        publish = ''
        standard = ''

        index =1
        for d in div:
            s = '/html/body/div[4]/div/div['+str(index)+']/span[1]/text()'
            spans = selector.xpath(s).extract()
            for span in spans:
                 # 作者
                if span == u"作者：":
                    author = selector.xpath('/html/body/div[4]/div/div['+str(index)+']/span[2]/a/text()').extract()
                    # print('author=%s' % author)
                elif span == u"作者单位：":
                    # 作者单位
                    author_unit = selector.xpath('/html/body/div[4]/div/div['+str(index)+']/span[2]/span/text()').extract()
                    author_unit_2 = selector.xpath('/html/body/div[4]/div/div['+str(index)+']/span[2]/text()').extract()
                    author_unit.extend(author_unit_2)
                    # print(author_unit)
                elif span == u'刊  名：':
                    article_name = selector.xpath('/html/body/div[4]/div/div['+str(index)+']/span[2]/a/text()').extract()
                    article_name_1 = selector.xpath('/html/body/div[4]/div/div['+str(index)+']/span[2]/span/span[1]/@title').extract()
                    article_name_2 = selector.xpath('/html/body/div[4]/div/div['+str(index)+']/span[2]/span/span[2]/@title').extract()
                elif span == u"年，卷(期)：":
                    years = selector.xpath('/html/body/div[4]/div/div['+str(index)+']/span[2]/a/text()').extract()
                    # print(years)
                elif span == u"分类号：":
                    classification = selector.xpath('/html/body/div[4]/div/div['+str(index)+']/span[2]/text()').extract()
                    # print(classification)
                elif span == u"关键词：":
                    keywords = selector.xpath('/html/body/div[4]/div/div['+str(index)+']/span[2]/a/text()').extract()
                    # print(keywords)
                elif span == u"在线出版日期：":
                    publish = selector.xpath('/html/body/div[4]/div/div['+str(index)+']/span[2]/text()').extract()
                    # print(publish)
                elif span == u"机标分类号：":
                    standard = selector.xpath('/html/body/div[4]/div/div['+str(index)+']/span[2]/text()').extract()
                    # print(standard)

            index = index+1
        # referenced = selector.xpath('/html/body/div[5]/div[1]/div[5]/div[2]/text()').extract()
        # reference = selector.xpath('/html/body/div[5]/div[1]/div[6]/div[2]/text()').extract()

        items = []
        item = WangfangItem()
        item['title'] = [c.encode('utf-8') for c in title]
        item['summary'] = [c.encode('utf-8') for c in summary]
        item['author'] = [c.encode('utf-8') for c in author]
        item['author_unit'] = [c.encode('utf-8') for c in author_unit]
        article_name.extend(article_name_1)
        article_name.extend(article_name_2)
        item['article_name'] = [c.encode('utf-8') for c in article_name]
        item['years'] = [c.encode('utf-8') for c in years]
        item['classification'] = [c.encode('utf-8') for c in classification]
        item['keywords'] = [c.encode('utf-8') for c in keywords]
        item['standard'] = [c.encode('utf-8') for c in standard]
        item['publish'] = [c.encode('utf-8') for c in publish]
        # item['referenced'] = [c.encode('utf-8') for c in referenced]
        # item['reference'] = [c.encode('utf-8') for c in reference]

        items.append(item)
        # return items

        '''
        下载文件
        '''
        download_page_link = selector.xpath('/html/body/div[3]/div/div[1]/a[1]/@href').extract()
        for d in download_page_link:
            yield scrapy.Request(d,meta={'title':title[0],'items':items},callback=self.parse_download)

    def parse_download(self,response):
        """
        下载pdf文件
        :param response:
        :return:
        """
        logger.info('-----------------下载期刊----------------------')
        sel = Selector(response)
        download_url = sel.xpath('//*[@id="doDownload"]/@href').extract()
        url = download_pre + download_url[0]

        title = response.meta['title']
        title_trip = title.strip()
        fileName = localDir + title_trip + '.pdf'
        # print('fileName = %s'%fileName)

        try:
            urllib.urlretrieve(url,fileName)
        except Exception,e:
            print e
            logger.info(e)

        return response.meta['items']


if __name__ == '__main__':
    scrapy.cmdline.execute(argv=['scrapy', 'crawl', 'wf'])
