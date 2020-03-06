# -*- coding: utf-8 -*-
import custom_settings
import scrapy
from price.items import PriceItem
from scrapy.http import FormRequest


class PriceSpider(scrapy.Spider):

    name = 'price'
    allowed_domains = custom_settings.ALLOWED_DOMAINS
    start_urls = custom_settings.START_URLS

    def parse(self, response):
        token = response.xpath('//*[@name="_csrf-frontend"]/@value').extract_first()
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                'LoginForm[username]': custom_settings.USER_LOGIN,
                'LoginForm[password]': custom_settings.USER_PASSWORD,
                '_csrf-frontend': token
            },
            callback=self.page_parser,
            dont_filter=True,
        )

    def page_parser(self, response):
        item = PriceItem()

        for row in response.xpath('//tbody/tr'):
            if row.xpath('th[2]//a//text()').extract_first():
                service = row.xpath('th[2]//a//text()').extract_first(),
            else:
                item = {
                    'service': service,
                    'title': row.xpath('td[2]//text()').extract_first(),
                    'price': row.xpath('td[3]//text()').extract_first(),
                }

                yield item
