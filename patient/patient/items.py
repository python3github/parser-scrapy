# -*- coding: utf-8 -*-
import scrapy


class PatientItem(scrapy.Item):

    id = scrapy.Field()
    second_name = scrapy.Field()
    first_name = scrapy.Field()
    patronymic = scrapy.Field()
    age = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    birthday = scrapy.Field()
