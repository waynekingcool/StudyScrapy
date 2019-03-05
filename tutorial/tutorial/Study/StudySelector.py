# <html>
#  <head>
#   <base href='http://example.com/' />
#   <title>Example website</title>
#  </head>
#  <body>
#   <div id='images'>
#    <a href='image1.html'>Name: My image 1 <br /><img src='image1_thumb.jpg' /></a>
#    <a href='image2.html'>Name: My image 2 <br /><img src='image2_thumb.jpg' /></a>
#    <a href='image3.html'>Name: My image 3 <br /><img src='image3_thumb.jpg' /></a>
#    <a href='image4.html'>Name: My image 4 <br /><img src='image4_thumb.jpg' /></a>
#    <a href='image5.html'>Name: My image 5 <br /><img src='image5_thumb.jpg' /></a>
#   </div>
#  </body>
# </html>

# 1.执行脚本 scrapy shell https://docs.scrapy.org/en/latest/_static/selectors-sample1.html
# 2.通过response.xpath("title/text()').getall()获取内容

# 获取图片地址
# response.css('img').xpath('@src').getall()

# 获取a里面的text
# response.xpath('//div[@id="images"]/a/text()').get()  response.css('div').css('a::text').get()
# 可以判断是否为空 response.xpath('//div[@id="images"]/a/text()').get() is None
# 如果为空还可以设置默认值 response.xpath('//div[@id="images"]/a/text()').get(default='not-found')

# 查找属性
# response.css('img').xpath('@src').getall()
# [img.attrib['src'] for img in response.css('img')
# response.css('base').attrib['href'] 该方法比较适用于一个结果的情况

# 查询所有属性 response.css('base').attrib

# <div class="quote">
#     <span class="text">“The world as we have created it is a process of our
#     thinking. It cannot be changed without changing our thinking.”</span>
#     <span>
#         by <small class="author">Albert Einstein</small>
#         <a href="/author/Albert-Einstein">(about)</a>
#     </span>
#     <div class="tags">
#         Tags:
#         <a class="tag" href="/tag/change/page/1/">change</a>
#         <a class="tag" href="/tag/deep-thoughts/page/1/">deep-thoughts</a>
#         <a class="tag" href="/tag/thinking/page/1/">thinking</a>
#         <a class="tag" href="/tag/world/page/1/">world</a>
#     </div>
# </div>

import json

class BookItem:
    def __init__(self,name, chapter_name, chapter_content, chapter_no):
        self.name = name
        self.chapter_name = chapter_name
        self.chapter_content = chapter_content
        self.chapter_no = chapter_no

jsonfile = open('../../book2.json',encoding='utf-8')
content = json.load(jsonfile)

# print(type(content))

# s2 = sorted(content, key=lambda item:item['chapter_no'])
#
# for item in s2:
#     print('chapNo: %s' % item['chapter_no'])

booktitle = ''

content.sort(key=lambda no: no['chapter_no'][0])
for item in content:
    booktitle = item['name']
    print('chapNo: %s' % item['chapter_no'])


# 写到本地中
# l = ['one', 'two', 'three']
# my_open = open('testxxx.txt','a')
#
# for string in l:
#     my_open.write(string)
#
# my_open.close()


my_open = open('abc.txt','a')

for dic in content:
    content = dic['chapter_content']
    chap_title = dic['chapter_name']
    my_open.write('%s %s' % (chap_title,content))
my_open.write('aaa')
my_open.close()



