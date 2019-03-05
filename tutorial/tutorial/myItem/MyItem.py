import scrapy


class MyItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()