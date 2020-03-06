# -*- coding: utf-8 -*-
import custom_settings
import scrapy
from scrapy.http import FormRequest
from specialist.items import SpecialistItem


class SpecialistSpider(scrapy.Spider):

    name = 'specialist'
    allowed_domains = custom_settings.ALLOWED_DOMAINS
    start_urls = custom_settings.START_URLS

    def parse(self, response):
        token = response.xpath(
            '//*[@name="_csrf-frontend"]/@value').extract_first()
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                'LoginForm[username]': custom_settings.USER_LOGIN,
                'LoginForm[password]': custom_settings.USER_PASSWORD,
                '_csrf-frontend': token},
            callback=self.page_parser,
            dont_filter=True,
        )

    def page_parser(self, response):
        item = SpecialistItem()

        for row in response.xpath('//tbody/tr'):
            item = {
                'second_name': row.xpath('td[1]//text()').extract_first(),
                'first_name': row.xpath('td[2]//text()').extract_first(),
                'patronymic': row.xpath('td[3]//text()').extract(),
                'phone': row.xpath('td[6]//text()').extract_first(),
            }

            yield item
        """
        page_link = response.xpath('//ul/li[last()]/a[@class="page-link"]/@href').extract_first()

        if page_link is not None and '#' not in page_link:
            yield response.follow(
                page_link,
                self.page_parser,
                dont_filter=True)
        """
