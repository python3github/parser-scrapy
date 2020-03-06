# -*- coding: utf-8 -*-
import custom_settings
import scrapy
from patient.items import PatientItem
from scrapy.http import FormRequest


class PatientSpider(scrapy.Spider):

    name = 'patient'
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
        item = PatientItem()
        for row in response.xpath('//tbody/tr'):
            item = {
                'id': row.xpath('td[1]//a/@href').re_first(r'id=\s*(.*)'),
                'second_name': row.xpath('td[1]//text()').extract_first(),
                'first_name': row.xpath('td[2]//text()').extract_first(),
                'patronymic': row.xpath('td[3]//text()').extract(),
                'age': row.xpath('td[4]//text()').extract_first(),
                'phone': row.xpath('td[5]//text()').extract_first(),
            }
            patient_detail_link = row.xpath('td[6]//a[1]/@href').extract_first()
            if patient_detail_link:
                link = 'https://{}{}'.format(
                    self.allowed_domains[0], patient_detail_link)
                request = scrapy.Request(
                    link,
                    callback=self.patient_detail_parser,
                    dont_filter=True
                )
                request.meta['item'] = item
                yield request

        page_link = response.xpath(
            '//ul/li[last()]/a[@class="page-link"]/@href').extract_first()
        if (page_link is not None) and ('#' not in page_link):
            yield response.follow(
                page_link,
                self.page_parser,
                dont_filter=True)

    def patient_detail_parser(self, response):
        item = response.meta['item']
        item['email'] = response.xpath(
            '//input[@id="patients-email"]/@value').extract_first()
        item['birthday'] = response.xpath(
            '//input[@id="patients-birthday"]/@value').extract_first()
        yield item
