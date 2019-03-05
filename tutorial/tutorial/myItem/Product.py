import scrapy

# class Product(scrapy.Item):
#     name = scrapy.Field()
#     price = scrapy.Field()
#     stock = scrapy.Field()
#     last_updated = scrapy.Field(serializer=str)
#
# product = Product(name="Desktop PC", price=1000)
# print(product)
# print(product['name'])
# print(product['price'])
# print( 'name' in product)
# print('last_updated' in product)
#
# product['last_updated'] = 'today'
# print(product['last_updated'])
#
# print(product.keys())
# print(product.items())


from scrapy.loader.processors import Join, MapCompose, TakeFirst
# remove_tags移除html标签
from w3lib.html import remove_tags

def filiter_price(value):
    if value.isdigit():
        return value

class Product(scrapy.Item):
    name = scrapy.Field(
        # 数据的输入输出处理
        input_processor = MapCompose(remove_tags),
        output_processor = Join(),
    )

    price = scrapy.Field(
        input_processor = MapCompose(remove_tags, filiter_price),
        output_processor = TakeFirst(),
    )

    stock = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)