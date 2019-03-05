import scrapy
from scrapy.http import Request
from tutorial.myItem.PropertiesItem import PropertiesItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
from urllib.parse import urlparse, urljoin
import socket
import datetime

# 使用指令 scrapy parse --spider=basic http://localhost:9312/properties/property_000000.html 可以显示出抓取的项目和请求
# 爬虫在两个方向移动 水平: 从索引页到另一个索引页   垂直: 从索引页面到列表页面提取项目
# scrapy crawl manual -s CLOSESPIDER_ITEMCOUNT=90  抓取90个结束

class fast(scrapy.Spider):
    name = 'fast'
    allowed_domains = ["localhost"]
    start_urls = [
        'http://localhost:9312/properties/index_00000.html',
    ]

    def parse(self, response):
        # 获取下一个url 并且yield request
        next_selector = response.xpath('//*[contains(@class,"next")]//@href')
        for url in next_selector.extract():
            yield Request(urljoin(response.url, url))

        # Iterate through products and create PropertiesItems
        selectors = response.xpath(
            '//*[@itemtype="http://schema.org/Product"]')
        for selector in selectors:
            yield self.parse_item(selector, response)


    def parse_item(self, selector, response):
        # 可使用scrapy check basic检查是否满足以下协议
        """ This function parses a property page.
        @url http://localhost:9312/properties/property_000000.html
        @returns items 1
        @scrapes title price description address image_URL
        @scrapes url project spider server date http://localhost:9312/properties/index_00000.html
        """
        l = ItemLoader(item=PropertiesItem(), selector=selector)
        # unicode.strip去掉空格 unicode.title开头字母大写
        l.add_xpath('title', './/*[@itemprop="name"][1]/text()', MapCompose(str.strip, str.title))
        # 去掉空格, 转化为float
        l.add_xpath('price', './/*[@itemprop="price"][1]/text()', MapCompose(lambda i: i.replace(',',''), float) , re='[.0-9]+')
        #
        l.add_xpath('description', './/*[@itemprop="description"][1]/text()', MapCompose(str.strip), Join())
        l.add_xpath('address', './/*[@itemtype="http://schema.org/''Place"][1]/text()', MapCompose(str.strip))
        l.add_xpath('image_URL', './/*[@itemprop="image"][1]/@src', MapCompose(lambda i:urljoin(response.url, i)))

        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.datetime.now())
        return l.load_item()

        return l.load_item()

