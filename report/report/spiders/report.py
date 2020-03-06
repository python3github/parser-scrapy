# -*- coding: utf-8 -*-
import custom_settings
import scrapy
from report.items import ReportItem
from scrapy.http import FormRequest


class ReportSpider(scrapy.Spider):

    name = 'report'
    allowed_domains = custom_settings.ALLOWED_DOMAINS
    start_urls =  custom_settings.START_URLS

    def parse(self, response):
        token = response.xpath(
            '//*[@name="_csrf-frontend"]/@value').extract_first()
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                'LoginForm[username]': custom_settings.USER_LOGIN,
                'LoginForm[password]': custom_settings.USER_PASSWORD,
                '_csrf-frontend': token},
            callback=self.after_login,
            dont_filter=True,
        )

    def after_login(self, response):
        token = response.xpath(
            '//*[@name="_csrf-frontend"]/@value').extract_first()
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                #form_search::first_row
                'ReportSearch[date_from]': '01.01.2019',
                'ReportSearch[date_to]': '30.08.2019',
                'ReportSearch[report_type]': '1',
                'ReportSearch[department_id]': '',
                'ReportSearch[entrance_id]': '',
                'ReportSearch[registry_id]': '',
                #form_search::second_row
                'ReportSearch[price_name]': 'ulthera',
                'ReportSearch[responsible_name]': '',
                'ReportSearch[patient_name]': '',
                '_csrf-frontend': token},
            callback=self.page_parser,
            dont_filter=True,
        )


    def page_parser(self, response):
        item = ReportItem()

        for row in response.xpath('//tbody/tr'):
            item = {
                'name': row.xpath('td[1]//text()').extract_first(),
                'worker': row.xpath('td[2]//text()').extract_first(),
                'ticket': row.xpath('td[3]//text()').extract(),
                'quantity': row.xpath('td[4]//text()').extract_first(),
                'price': row.xpath('td[5]//text()').extract_first(),
                'discount': row.xpath('td[6]//text()').extract_first(),
                'total': row.xpath('td[7]//text()').extract_first(),
                'cost_price': row.xpath('td[8]//text()').extract_first(),
            }

            phone_page_link = row.xpath('td[1]/a/@href').extract_first()

            if phone_page_link is not None:
                link = response.urljoin(phone_page_link)
                request = scrapy.Request(
                    link,
                    callback=self.phonenumber,
                    dont_filter=True)
                request.meta['item'] = item
                yield request

    def phonenumber(self, response):
        item = response.meta['item']
        item['date'] = response.xpath(
            '//table[@id="w0"]//tr/th[text()="Дата рождения"]/following-sibling::*/text()').extract_first()
        item['phone'] = response.css('.phone-link::text').extract_first()
        yield item
