# -*- coding: utf-8 -*-
import scrapy


class SpecialistItem(scrapy.Item):

    second_name = scrapy.Field()
    first_name = scrapy.Field()
    patronymic = scrapy.Field()
    phone = scrapy.Field()
