# -*- coding: utf-8 -*-
import json

import custom_settings
import scrapy
from receipt.items import ReceiptItem
from scrapy.http import FormRequest


class ReceiptSpider(scrapy.Spider):

    name = 'receipt'
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
            callback=self.page_parser,
            dont_filter=True,
        )


    def page_parser(self, response):
        item = ReceiptItem()

        for row in response.xpath('//tbody/tr'):
            item = {
                'date': row.xpath('td[2]//text()').extract_first().strip(),
                'document_id': row.xpath('td[3]//a/@data-receipt-id').extract_first(),
                'patient_id': row.xpath('td[4]//a/@href').re_first(r'id=\s*(.*)'),
                'patient': row.xpath('td[4]//text()').extract_first(),
                'amount': row.xpath('td[5]//text()').extract_first().strip(),
                'cash': row.xpath('td[6]//text()').extract_first().strip(),
                'cart': row.xpath('td[7]//text()').extract_first().strip(),
                'bank': row.xpath('td[8]//text()').extract_first().strip(),
            }

            document_id = row.xpath('td[3]//a/@data-receipt-id').extract_first()

            if document_id:
                link = 'https://{}/finance/receipt/receipt?id={}'.format(
                    self.allowed_domains[0],
                    document_id
                )
                request = scrapy.Request(
                    link,
                    callback=self.document,
                    dont_filter=True
                )
                request.meta['item'] = item
                yield request


    def document(self, response):
        item = response.meta['item']
        data = json.loads(response.text)
        sel = scrapy.Selector(text=data['html'], type="html")
        count = len(sel.xpath('//div[@class="row mb-2 receipt__item"]'))

        if count:
            # если квитанция
            i = 0
            s = 0
            for row in sel.xpath('//div[@class="row mb-2 receipt__item"]'):
                # если у квитанции несколько рядов
                item['procedure'] = row.xpath(
                    '//div[@class="fake-disable-input"]/text()')[i].extract()
                i += 1
                item['procedure_quantity'] = row.xpath(
                    '//div[@class="fake-disable-input"]/text()')[i].extract()
                i += 1
                item['procedure_discount'] = row.xpath(
                    '//div[@class="fake-disable-input"]/text()')[i].extract()
                i += 1
                item['procedure_price'] = row.xpath(
                    '//div[@class="fake-disable-input"]/text()')[i].extract()
                i += 1
                item['procedure_amount'] = row.xpath(
                    '//div[@class="fake-disable-input receipt__item-sum"]/text()')[s].extract()
                s += 1

                if row.xpath(
                    '//select[@class="form-control receipt__item-doctor"]//option[@selected]/text()'):

                    item['procedure_specialist'] = row.xpath(
                        '//select[@class="form-control receipt__item-doctor"]//option[@selected]/text()').extract_first()

                elif row.xpath('//div[@class="fake-disable-input"]/text()')[i]:

                    item['procedure_specialist'] = row.xpath(
                        '//div[@class="fake-disable-input"]/text()')[i].extract()
                    i += 1

                yield item

        else:
            # если подарочный сертификат
            yield item
