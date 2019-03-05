import scrapy
from scrapy.item import Item, Field
from scrapy.loader.processors import Join, MapCompose, TakeFirst




class Book(scrapy.Item):
    name = scrapy.Field()
    chapter_name = scrapy.Field()
    chapter_content = scrapy.Field(
        output_processor=Join(),
    )
    chapter_no = scrapy.Field()

