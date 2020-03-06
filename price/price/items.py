# -*- coding: utf-8 -*-
import scrapy


class PriceItem(scrapy.Item):

    title = scrapy.Field()
    service = scrapy.Field()
    price = scrapy.Field()
