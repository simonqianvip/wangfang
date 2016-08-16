# -*- coding: utf-8 -*-

import json
import codecs
import logging
from scrapy import signals
from twisted.enterprise import adbapi
from datetime import datetime
import MySQLdb
import MySQLdb.cursors

logger = logging.getLogger(__name__)

class WangfangPipeline(object):
    def __init__(self):
        try:
            self.file = codecs.open('C:\Users\simon\Desktop\\wangfang.json', 'wb', encoding='utf-8')
        except IOError, msg:
            print(msg)
            raise

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line.decode("unicode_escape"))
        # self.file.close()
        return item



class MySQLStoreFmPipeline(object):
    """
    数据存储到mysql
    """
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        '''
        从settings文件加载属性
        :param settings:
        :return:
        '''
        dbargs = dict(
                host=settings['MYSQL_HOST'],
                db=settings['MYSQL_DBNAME'],
                user=settings['MYSQL_USER'],
                passwd=settings['MYSQL_PASSWD'],
                charset='utf8',
                cursorclass=MySQLdb.cursors.DictCursor,
                use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    # pipeline默认调用
    def process_item(self, item, spider):
        deferred = self.dbpool.runInteraction(self._do_insert, item, spider)
        deferred.addErrback(self._handle_error)
        # d.addBoth(lambda _: item)
        return deferred

    # 将每行更新或写入数据库中
    def _do_insert(self, conn, item, spider):
        '''
        id              int(11)  (NULL)           NO      PRI     (NULL)   auto_increment  select,insert,update,references  主键
        title           text     utf8_general_ci  YES             (NULL)                   select,insert,update,references  标题
        summary         text     utf8_general_ci  YES             (NULL)                   select,insert,update,references  摘要
        author          text     utf8_general_ci  YES             (NULL)                   select,insert,update,references  作者
        author_unit     text     utf8_general_ci  YES             (NULL)                   select,insert,update,references  作者单位
        article_name    text     utf8_general_ci  YES             (NULL)                   select,insert,update,references  刊名
        years           text     utf8_general_ci  YES             (NULL)                   select,insert,update,references  年卷
        classification  text     utf8_general_ci  YES             (NULL)                   select,insert,update,references  分类
        keywords        text     utf8_general_ci  YES             (NULL)                   select,insert,update,references  关键词
        standard        text     utf8_general_ci  YES             (NULL)                   select,insert,update,references  机标分类号
        publish         text     utf8_general_ci  YES             (NULL)                   select,insert,update,references  出版日期
        '''
        title = ''
        for t in item['title']:
            title = title + t.strip()
        print title

        summary = ''
        for s in item['summary']:
            summary = summary + s.strip()
        print summary

        author = ''
        for a in item['author']:
            author = author + a.strip()+','
        print author

        author_unit = ''
        for a in item['author_unit']:
            author_unit = author_unit + a.strip() + ','
        print author_unit

        article_name = ''
        for a in item['article_name']:
            article_name = article_name + a.strip() + ','
        print article_name

        years = ''
        for y in item['years']:
            years = years + y.strip()
        print years

        classification = ''
        for c in item['classification']:
            classification = classification + c.strip() +','
        print classification

        keywords = ''
        for k in item['keywords']:
            keywords = keywords + k.strip()+','
        print keywords

        standard = ''
        for s in item['standard']:
            standard = standard + s.strip()
        print standard

        publish = ''
        for p in item['publish']:
            publish = publish + p.strip()
        print publish

        conn.execute("""
                insert into wf_info(title, summary, author, author_unit, article_name,years,classification,keywords,standard,publish)
                values(%s, %s, %s, %s, %s, %s,%s,%s,%s,%s)
        """, (title,summary ,author ,author_unit ,article_name,years,classification,keywords,standard,publish))

    def _handle_error(self, failue):
        logger.error(failue)
