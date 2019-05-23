# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

class YunqispiderPipeline(object):
    def __init__(self):
        self.conn = pymysql.Connect(
            host='localhost',  # 数据库ip
            port=3306,  # 数据库端口号
            user='root',  # 数据库用户名
            passwd='root',  # 数据库密码
            db='yunqi',  # 要连接的数据库名
            charset='utf8',  # 编码
        )
        # 创建数据库游标操作数据库语句
        self.cursor = self.conn.cursor()
        self.sql = """create table if not exists yunqibook (
                      id int primary key auto_increment,
                      author varchar(20), name varchar(56),
                      last_update_time varchar(20), classify varchar(20),
                      all_clicks varchar(10), all_popularity varchar(10),
                      all_recommend varchar(10), word_number varchar(10),
                      all_comments varchar(10), status varchar(10), summary varchar(1024))"""
        self.cursor.execute(self.sql)

    def open_spider(self, spider):
        print('爬虫开始')

    def close_spider(self, spider):
        # 爬虫停止的时候关闭数据库
        self.conn.close()
        print('{}爬虫已停止'.format(self.__class__))

    def process_item(self, item, spider):
        author = item['author']
        last_update_time = item['last_update_time']
        name = item['name']
        classify = item['classify']
        all_clicks = item['all_clicks']
        all_popularity = item['all_popularity']
        all_recommend = item['all_recommend']
        word_number = item['word_number']
        all_comments = item['all_comments']
        status = item['status']
        summary = item['summary']

        sql = """insert into yunqibook (author, last_update_time, name, classify, all_clicks,
                 all_popularity, all_recommend, word_number, all_comments, status, summary)
                 values('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"""
        self.conn.ping(reconnect=True)
        self.cursor.execute(sql.format(author, last_update_time, name, classify, all_clicks,
                                       all_popularity, all_recommend, word_number, all_comments, status, summary))

        self.conn.commit()
