import time

import scrapy
from scrapy.item import Item, Field

prefix_url = 'https://find-and-update.company-information.service.gov.uk'

class CustomItem(Item):
    name = Field()
    company_number = Field()
    registered_office_address = Field()
    company_status = Field()
    company_type = Field()
    company_creation_date = Field()
    nature_of_business = Field()
    time = Field()


class MySpider(scrapy.Spider):
    name = 'spider_govuk'
    allowed_domains = ['find-and-update.company-information.service.gov.uk']

    def start_requests(self):
        yield scrapy.Request('https://find-and-update.company-information.service.gov.uk/search/companies?q=software', self.parse)
        yield scrapy.Request('https://find-and-update.company-information.service.gov.uk/search/companies?q=food', self.parse)
        yield scrapy.Request('https://find-and-update.company-information.service.gov.uk/search/companies?q=all', self.parse)


    def parse(self, response):
        for href in response.xpath('//*[@id="results"]/li/h3/a/@href').getall():
            self.logger.info('Path response: %s', response)
            self.logger.info('Path specifico: %s', href)
            self.logger.info(response.urljoin(str(href)))
            yield scrapy.Request(response.urljoin(str(href)), self.information_companies)
        for next_page in response.css('#next-page'):
            yield response.follow(next_page, self.parse)


    def information_companies(self, response):
        start_time = time.time()
        item = CustomItem()
        item['name'] = self.split_and_replace(response.xpath('//*[@id="content-container"]/div[1]/p[1]/text()').get())
        item['company_number'] = self.split_and_replace(response.xpath('//*[@id="company-number"]/strong/text()').get())
        item['registered_office_address'] = self.split_and_replace(response.xpath('//div[@class="govuk-tabs__panel"]/dl/dd/text()').get())
        item['company_status'] = self.split_and_replace(response.xpath('//*[@id="company-status"]/text()').get())
        item['company_type'] = self.split_and_replace(response.xpath('//*[@id="company-type"]/text()').get())
        item['company_creation_date'] = self.split_and_replace(response.xpath('//*[@id="company-creation-date"]/text()').get())
        item['nature_of_business'] = self.split_and_replace(response.xpath('//*[@id="sic0"]/text()').get())
        end_time = time.time()
        item['time'] = end_time - start_time
        return item


    def split_and_replace(self, text):
        text = text.strip()
        text = text.replace("\n", "")
        return text


