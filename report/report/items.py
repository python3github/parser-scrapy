# -*- coding: utf-8 -*-
import scrapy


class ReportItem(scrapy.Item):

    name = scrapy.Field()
    phone = scrapy.Field()
    date = scrapy.Field()
    worker = scrapy.Field()
    ticket = scrapy.Field()
    quantity = scrapy.Field()
    price = scrapy.Field()
    discount = scrapy.Field()
    total = scrapy.Field()
    cost_price = scrapy.Field()
