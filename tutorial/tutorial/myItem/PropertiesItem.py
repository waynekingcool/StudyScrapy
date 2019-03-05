import scrapy
from scrapy.item import Item, Field

class PropertiesItem(scrapy.Item):
    title = Field()
    price = Field()
    description = Field()
    address = Field()
    image_URL = Field()

    # calcuated field
    images = Field()
    location = Field()

    # housekeepint field
    url = Field()
    project = Field()
    spider = Field()
    server = Field()
    date = Field()