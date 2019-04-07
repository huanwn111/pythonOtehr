# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DangdangItem(scrapy.Item):#【项目没改，用了豆瓣的，本例是当当注意】
    # define the fields for your item here like:
    # name = scrapy.Field()
    #【（）里继承自scrapy.Item类，继承scrapy.Item，可以通过scrapy中心引擎整体调度。
    #例如本例把数据用.Field()类封装成自定义字典的格式。
    # 定义封装数据属性(使用时可以通过doubanItemNew实例['bookName']=...把数据统一到Item中，
    # 最后yield返回，scrapy中心引擎再发给pipline做存储处理。
    # 类似于session会话的整体。
    # 语法似thinkphp java的entity等，所有的框架都差不多。
    # 先不要多想)】

    #定义格式参考
    # name = scrapy.Field()
    bookName = scrapy.Field()
    #【class Field(dict): Field类的作用是实现让数据能以类似字典的形式记录和访问传递
    #所以，只需指定属性名，套上这种格式即可。】
    num = scrapy.Field()
    author = scrapy.Field()
    price = scrapy.Field()

    pass