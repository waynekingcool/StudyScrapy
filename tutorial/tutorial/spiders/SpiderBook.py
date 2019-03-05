import scrapy
from scrapy.http import Request
from urllib.parse import urlparse, urljoin
from tutorial.myItem.Book import Book
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider
import re
# 1.列表页:https://m.bingdianshuwu.com/top/goodnum_1/
# 2.进入小说开始阅读 页 https://m.bingdianshuwu.com/info-968/
# 3.小说章节列表页 https://m.bingdianshuwu.com/wapbook-968/


class SpiderBook(scrapy.Spider):
    name = 'book'

    bookChapList = []
    urlpath = ''

    def start_requests(self):
        urls = [
            # 'https://m.bingdianshuwu.com/wapbook-968/',
            'https://m.bingdianshuwu.com/wapbook-2329/',
        ]

        # 测试
        # yield Request(urls[0], callback=self.test)

        for url in urls:
            yield Request(url,callback=self.get_chapList)

    def parse(self, response):
        book_urls = response.xpath('//li/a[@class="l mr10"]/@href').getall()
        for book_url in book_urls:
            yield Request(book_url, callback=self.parse_read)


    def get_chapList(self, response):
        temp_array = response.xpath('//*[@class="chapter"]//@href').getall()
        for url in temp_array:
            # 添加到数组中
            self.bookChapList.append(url)

        # 判断是否为最后一页
        title_array = response.xpath('//*[@class="page"]/a//text()').getall()
        url_array = response.xpath('//*[@class="page"]//@href').getall()

        if len(title_array) == 2:
            if ('首页' in title_array) and ('上一页' in title_array):
                # 最后一页
                self.log('最后一页=首页 上一页')
                # 开始获取开始阅读url
                for urlxx in self.bookChapList:
                    self.log('正在获取%s的内容....' % urlxx)
                    yield Request(urlxx,callback=self.get_content)

                # 测试
                # self.log('正在获取%s的内容....' % self.bookChapList[0])
                # yield Request(self.bookChapList[0], callback=self.get_content)

                # for index,value in enumerate(self.bookChapList):
                #     self.log('URL%d:  %s' % (index,value))
                # raise CloseSpider('最后一页,终止爬行')
            else:
                self.log('首页=下一页 尾页')
                # url = url_array[0];
                urlxx = urljoin(response.url,url_array[0])
                yield Request(urlxx,callback=self.get_chapList)

        elif len(title_array) == 4:
            # 中间继续往下爬
            self.log('中间页=首页 上一页 下一页 尾页')
            urlxx = urljoin(response.url,url_array[2])
            yield Request(urlxx,callback=self.get_chapList)

    def get_content(self, response):

        # 判断是否抓取完毕
        nextstr = response.xpath('//a[@id="pb_next"]//text()').get()
        if nextstr == '下一页':

            # 获取小说名称
            l = ItemLoader(item=Book(), response=response)
            l.add_xpath('name', '//h1[@id="_52mb_h1"]//text()')
            l.add_xpath('chapter_name', '//div[@id="nr_title"]//text()')


            if response.meta is not None:
                if 'item' in response.meta.keys():
                    item = response.meta['item']
                    l.add_value('chapter_content', item['chapter_content'])
                else:
                    l.add_xpath('chapter_content', '//div[@id="nr1"][1]/text()')


            temp = urlparse(response.url)
            l.add_value('chapter_no', temp.path)

            # 下一页url  meta用于传递参数
            temp_url = response.xpath('//a[@id="pb_next"]//@href').get()
            urlstr = urljoin(response.url, temp_url)
            yield Request(urlstr, callback=self.get_content,meta={'item':l.load_item()})
        else:
            # 获取小说名称
            l = ItemLoader(item=Book(), response=response)
            l.add_xpath('name', '//h1[@id="_52mb_h1"]//text()')

            # 处理标题
            title = response.xpath('//div[@id="nr_title"]//text()').get()
            s = re.search('第(.*)第',title)
            s = s.group()
            s = s[0:-1]
            # s = '\n \t %s \n \t' % s
            l.add_value('chapter_name',s)


            # l.add_xpath('chapter_name', '//div[@id="nr_title"]//text()')

            item = response.meta['item']
            l.add_value('chapter_content',item['chapter_content'])

            l.add_xpath('chapter_content', '//div[@id="nr1"][1]/text()')

            # 对编号进行处理
            temp = urlparse(response.url)
            no = temp.path
            no = no[14:-7]
            l.add_value('chapter_no', no)

            yield l.load_item()






