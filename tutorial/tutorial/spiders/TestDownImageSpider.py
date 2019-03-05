import scrapy
from tutorial.myItem.MyItem import MyItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
from urllib.parse import urlparse, urljoin


# 测试自动下载图片 记得在setting里面做相关配置
class TestDownloadImagesSpider(scrapy.Spider):
    name = 'downImage'
    allowed_domains = ["localhost"]
    start_urls = [
        'http://localhost:9312/properties/property_000000.html',
    ]

    def parse(self, response):
        l = ItemLoader(item=MyItem(), response=response)
        l.add_xpath('image_urls', '//*[@itemprop="image"]//@src', MapCompose(lambda i:urljoin(response.url,i)))
        return l.load_item()