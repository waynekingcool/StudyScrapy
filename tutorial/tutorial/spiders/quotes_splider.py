import scrapy

# 指令
# 1.进入最上级文件夹 输入 scrapy crawl quotes抓取内容  scrapy crawl quotes -o quotes.json将数据保存为json
# 2.学习抓取数据的最好方式就是通过scrapy shell进行抓取 scrapy shell 'http://quotes.toscrape.com/page/1/'

class QuotesSpider(scrapy.Spider):
    # 定义的Spider的名称,在整个项目中必须是唯一的
    name = 'quotes'

    # 返回一个可以迭代的请求
    # def start_requests(self):
    #     urls = [
    #         'http://quotes.toscrape.com/page/1/',
    #         'http://quotes.toscrape.com/page/2/',
    #     ]
    #
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    # 简写,可以不用写start_request方法,
    # start_urls = [
    #     'http://quotes.toscrape.com/page/1/',
    #     'http://quotes.toscrape.com/page/2/',
    # ]

    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]


    # 处理请求,response是TextResponse的一个实例,其中保存着页面的内容,并且有很多有用的方法去处理数据
    # parse()方法通常解析返回,获取抓取的数据,以字典的方式,并且找到新的urls去进行抓取
    # def parse(self, response):
    #     page = response.url.split("/")[-2]
    #     print('page is '+page)
    #     filename = 'quotes-%s.html' % page
    #     with open(filename,'wb') as f:
    #         f.write(response.body)
    #     self.log('Saved file %s' % filename)

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text':quote.css('span.text::text').get(),
                'author':quote.css('small.author::text').get(),
                'tags':quote.css('div.tags a.tag::text').getall(),
            }

        for a in response.css('li.next a'):
            yield response.follow(a, callback=self.parse)

        # next_page = response.css('li.next a::attr(href)').get()
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)

            # next_page = response.urljoin(next_page)
            # print('next_page %s' % next_page )
            # yield scrapy.Request(next_page, callback=self.parse)
    # scrapy shell
    # response.css('title::text').getall()  获取内容
    # response.css('title').getall()  获取整个标签 ==> ['<title>Quotes to Scrape</title>'] getall()获取列表  get()获取第一条数据
    # b = re.sub(r'\s+','', a) 去除空格和换行