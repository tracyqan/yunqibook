# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis import spiders

from yunqiSpider.items import YunqispiderItem


class YunqiSpider(spiders.RedisSpider):
    name = 'yunqi'
    allowed_domains = ['yunqi.qq.com']
    # start_urls = ['http://yunqi.qq.com/bk/so2/n10p1']
    redis_key = 'yunqi:start_urls'

    def parse(self, response):
        """
        完成主页面的数据爬取，爬取详情页的url，下一页的url，小说的基本信息
        :param response:
        :return:
        """
        print('当前请求头：{}'.format(response.request.headers['User-Agent']))
        next_page_a = response.xpath('//div[@id="pageHtml2"]/a[last()]')
        if next_page_a.xpath('./span[@class="page-next"]'):
            next_page_url = next_page_a.xpath('./@href').get()
            yield scrapy.Request(next_page_url, callback=self.parse)
        story_list_divs = response.xpath('//div[@id="detailedBookList"]/div') # 获取当前页小说列表中所有的小说div标签
        for i in story_list_divs:
            # 遍历每一个小说div标签, 获取详情页url,小说的基本信息
            detail_url = i.xpath('./a/@href').get() # 详情页url
            author = i.xpath('./div[@class="book_info"]/dl[1]/dd[1]/a/text()').get()  # 小说作者
            last_update_time = i.xpath('./div[@class="book_info"]/dl[2]/dd[1]/text()').get()  # 最后更新时间
            basic_info = {
                'author': author,
                'last_update_time': last_update_time,
            }
            yield scrapy.Request(detail_url, callback=self.parse_detail, meta=basic_info)



    def parse_detail(self, response):
        try:
            author = response.meta['author'] # 小说作者
            last_update_time = response.meta['last_update_time'] # 小说最后更新时间
            name = response.xpath('//div[@class="main2"]//div[@class="title"]/strong/a/text()').get() # 小说名称
            classify = response.xpath('//div[@class="main2"]//div[@class="title"]/a[2]/text()').get() # 小说分类
            user_click = response.xpath('//div[@id="novelInfo"]//tr[2]/td/text()').getall() # 小说点击信息
            all_clicks = user_click[0].split('：')[-1] # 总点击
            all_popularity = user_click[1].split('：')[-1] # 总人气
            all_recommend = user_click[2].split('：')[-1] # 总推荐
            word_number = response.xpath('//div[@id="novelInfo"]//tr[5]/td[1]/text()').get().split('：')[-1]  # 小说当前总字数
            all_comments = response.xpath('//div[@id="novelInfo"]//tr[5]/td[2]/span/text()').get() # 小说评论数
            status = response.xpath('//div[@id="novelInfo"]//tr[5]/td[3]/span/text()').get() # 小说状态
            summary = ''.join(response.xpath('//div[@class="info"]//p/text()').getall()) # 小说简介

            item = YunqispiderItem(author=author, name=name, classify=classify, all_clicks=all_clicks,
                                   all_popularity=all_popularity, all_recommend=all_recommend, last_update_time=last_update_time,
                                   word_number=word_number, all_comments=all_comments, status=status, summary=summary)
            yield item
        except:
            pass  # 有部分小说不存在,网站小说列表并没有删除





if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl yunqi'.split())