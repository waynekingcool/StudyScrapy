# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import FormRequest

# 带有登录信息的spider
class LoginSpider(CrawlSpider):
    name = 'login'
    allowed_domains = ['web']
    # start_urls = ['http://web/']
    def start_requests(self):
        return [
            FormRequest(
                "http://localhost:9312/dynamic/login",
                formdata={"user": "user", "pass": "pass"}
            )
        ]

    # 提取链接LinkExtractor
    # rules = (
    #     Rule(LinkExtractor(restrict_xpaths='//*[contains(@class,"next")]')),
    #     Rule(LinkExtractor(restrict_xpaths='//*[@itemprop="url"]'),
    #          callback='parse_item')
    # )
    #
    # def parse_item(self, response):
    #     item = {}
    #     #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
    #     #item['name'] = response.xpath('//div[@id="name"]').get()
    #     #item['description'] = response.xpath('//div[@id="description"]').get()
    #     return item
