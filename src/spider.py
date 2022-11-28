import scrapy


prefix_url = 'https://en.wikipedia.org'

class MySpider(scrapy.Spider):
    name = 'spider_wiki'
    allowed_domains = ['en.wikipedia.org']
    start_urls = [
        prefix_url + '/wiki/Lists_of_companies',
    ]

    def parse(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
        for title in response.xpath('//div[@class="div-col"][1]/ul/li/a'):
            yield {'title': title.css('::text').get()}

        for href in response.xpath('//div[@class="div-col"][1]/ul/li/a/@href').getall():
            self.logger.info('Path specifico: %s', href)
            yield scrapy.Request(response.urljoin(str(href)), self.parse)

