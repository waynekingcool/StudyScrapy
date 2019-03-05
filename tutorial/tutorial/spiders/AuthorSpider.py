# import scrapy
# from tutorial.tutorial.myItem.Product import Product
# from scrapy.loader import ItemLoader
#
# class AuthorSpider(scrapy.Spider):
#     name = 'author'
#
#     start_urls = ['http://quotes.toscrape.com/']
#
#     def parse(self, response):
#         for href in response.css('.author + a::attr(href)'):
#             yield response.follow(href, self.parse_author)
#
#         for href in response.css('li.next a::attr(href'):
#             yield response.follow(href, self.parse)
#
#     def parse_author(self, response):
#         def extract_with_css(query):
#             return response.css(query).get(default='').strip()
#
#         yield {
#             'name': extract_with_css('h3.author-title::text'),
#             'birthdate': extract_with_css('.author-born-date::text'),
#             'bio': extract_with_css('.author-description::text'),
#         }
#
#     def parseTwo(self,response):
#         l = ItemLoader(item=Product(), response=response)
#         # 通过xpath方式填充数据
#         l.add_xpath('name', '//div[@class="productname"]')
#         l.add_xpath('name','//div[@class="producttitle"]')
#         l.add_xpath('price','//p[@id="price"]')
#         # 通过css选择器方式填充数据
#         l.add_css('stock','p#stock')
#         # 直接填充数据
#         l.add_value('last_updated','today')
#         # 当填充完数据后返回
#         return l.load_item()

