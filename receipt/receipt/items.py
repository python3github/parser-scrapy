# -*- coding: utf-8 -*-
import scrapy


class ReceiptItem(scrapy.Item):

    date = scrapy.Field()
    document_id = scrapy.Field()
    patient_id = scrapy.Field()
    patient = scrapy.Field()
    amount = scrapy.Field()
    cash = scrapy.Field()
    cart = scrapy.Field()
    bank = scrapy.Field()
    procedure = scrapy.Field()
    procedure_quantity = scrapy.Field()
    procedure_discount = scrapy.Field()
    procedure_price = scrapy.Field()
    procedure_amount = scrapy.Field()
    procedure_specialist = scrapy.Field()
