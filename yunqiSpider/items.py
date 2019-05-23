# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YunqispiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    author = scrapy.Field() # 小说作者
    last_update_time = scrapy.Field()   # 小说最后更新时间
    name = scrapy.Field()  # 小说名称
    classify = scrapy.Field()   # 小说分类
    user_clickuser_clickuser_click = scrapy.Field()  # 小说点击信息
    all_clicks = scrapy.Field()  # 总点击
    all_popularity = scrapy.Field()  # 总人气
    all_recommend = scrapy.Field()  # 总推荐
    word_number = scrapy.Field()  # 小说当前总字数
    all_comments = scrapy.Field()  # 小说评论数
    status = scrapy.Field()  # 小说状态
    summary = scrapy.Field()  # 小说简介