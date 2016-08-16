# -*- coding: utf-8 -*-
import subprocess
import scrapy


class MyDownloader(object):
    def process_request(self, response):
        # if request.url.endswith(".zip"):
        subprocess.Popen(["wget", response.url, "-P", "d:\\FireFox_Download"])
        return scrapy.http.HtmlResponse(url="", body="",
                                        encoding='utf8')  # 随便返回一个response对象，阻止其他midllware的 process_request方法继续运行，raise IgnoreRequest 也可以
