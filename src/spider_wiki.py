import scrapy
from scrapy.item import Item, Field


prefix_url = 'https://en.wikipedia.org'

class CustomItem(Item):
    name = Field()
    type = Field()
    industry = Field()
    founded = Field()
    founders = Field()
    headquarters = Field()
    key_people = Field()
    services = Field()
    revenue = Field()
    operating_income = Field()
    total_assets = Field()
    number_of_employees = Field()
    website = Field()


class MySpider(scrapy.Spider):
    name = 'spider_wiki'
    allowed_domains = ['en.wikipedia.org']

    def start_requests(self):
        yield scrapy.Request(prefix_url + '/wiki/List_of_the_largest_software_companies', self.parse2)
        yield scrapy.Request(prefix_url + '/wiki/List_of_companies_of_the_European_Union', self.parse2)
        yield scrapy.Request(prefix_url + '/wiki/List_of_largest_companies_by_revenue', self.parse1)
        yield scrapy.Request(prefix_url + '/wiki/List_of_bitcoin_companies', self.parse1)
        yield scrapy.Request(prefix_url + '/wiki/List_of_largest_biomedical_companies_by_market_capitalization', self.parse3)
        yield scrapy.Request(prefix_url + '/wiki/List_of_coffee_companies', self.parse1)
        yield scrapy.Request(prefix_url + '/wiki/List_of_bullion_dealers', self.parse1)
        yield scrapy.Request(prefix_url + '/wiki/List_of_film_production_companies', self.parse1)
        yield scrapy.Request(prefix_url + '/wiki/List_of_IT_consulting_firms', self.parse1)
        yield scrapy.Request(prefix_url + '/wiki/List_of_oil_exploration_and_production_companies', self.parse1)



    # parse1, parse2, parse3: sono metodi utilizzati per entrare in ulteriori pagine più specifiche attraverso
    # i link che sono presenti rispettivamente nella prima, seconda, terza colonna della tabella
    def parse1(self, response):
        for href in response.xpath('//table/tbody/tr/td[1]/a/@href').getall():
            self.logger.info('Path specifico: %s', href)
            yield scrapy.Request(response.urljoin(str(href)), self.title_name_companies)

    def parse2(self, response):
        for href in response.xpath('//table/tbody/tr/td[2]/a/@href').getall():
            self.logger.info('Path specifico: %s', href)
            yield scrapy.Request(response.urljoin(str(href)), self.title_name_companies)

    def parse3(self, response):
        for href in response.xpath('//table/tbody/tr/td[3]/a/@href').getall():
            self.logger.info('Path specifico: %s', href)
            yield scrapy.Request(response.urljoin(str(href)), self.title_name_companies)



    # features_companies: un metodo che consente di estrarre le informazioni di ogni singola azienda che sono
    # presenti nel box laterale a destra nella pagina di dettaglio
    def title_name_companies(self, response):
        item = CustomItem()
        item['name'] = response.xpath('//table[@class="infobox vcard"]/caption/text()').get()
        item['type'] = self.try_all_structure(response, "Type")
        item['industry'] = self.try_all_structure(response, "Industry")
        item['founded'] = self.try_all_structure(response, "Founded")
        #retrieve the Founder/Founders
        if len(self.try_all_structure(response, "Founders")) > 0:
            item['founders'] = self.try_all_structure(response, "Founders")
        else:
            item['founders'] = self.try_all_structure(response, "Founder")
        #retrive the Headquarters
        item['headquarters'] = self.try_all_structure(response, "Headquarters")
        item['key_people'] = self.try_all_structure(response, "Key people")
        item['services'] = self.try_all_structure(response, "Services")
        item['revenue'] = self.try_all_structure(response, "Revenue")
        item['operating_income'] = response.xpath('//table[@class="infobox vcard"]/tbody/tr/th/div/a[contains(text(), "Operating income")]/../../../td//text()').getall()
        item['total_assets'] = response.xpath('//table[@class="infobox vcard"]/tbody/tr/th/span/a[contains(text(), "Total assets")]/../../../td//text()').getall()
        item['number_of_employees'] = response.xpath('//table[@class="infobox vcard"]/tbody/tr/th/div[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "employees")]/../../td//text()').getall()
        item['website'] = self.try_all_structure(response, "Website")
        return item


    def try_all_structure(self, response, name):
        if len(response.xpath('//table[@class="infobox vcard"]/tbody/tr/th[contains(text(), "' + name +'")]/../td/div/ul/li/text()').getall()) > 0:
            return response.xpath('//table[@class="infobox vcard"]/tbody/tr/th[contains(text(), "' + name +'")]/../td/div/ul/li/text()').getall()
        elif len(response.xpath('//table[@class="infobox vcard"]/tbody/tr/th[contains(text(), "' + name +'")]/../td/div/ul/li/a/text()').getall()) > 0:
            return response.xpath('//table[@class="infobox vcard"]/tbody/tr/th[contains(text(), "' + name +'")]/../td/div/ul/li/a/text()').getall()
        elif len(response.xpath('//table[@class="infobox vcard"]/tbody/tr/th[contains(text(), "' + name +'")]/../td/a/text()').getall()) > 0:
            return response.xpath('//table[@class="infobox vcard"]/tbody/tr/th[contains(text(), "' + name +'")]/../td/a/text()').getall()
        elif len(response.xpath('//table[@class="infobox vcard"]/tbody/tr/th[contains(text(), "' + name +'")]/../td/div/a/text()').getall()) > 0:
            return response.xpath('//table[@class="infobox vcard"]/tbody/tr/th[contains(text(), "' + name +'")]/../td/div/a/text()').getall()
        elif len(response.xpath('//table[@class="infobox vcard"]/tbody/tr/th[contains(text(), "' + name +'")]/../td/div/text()').getall()) > 0:
            return response.xpath('//table[@class="infobox vcard"]/tbody/tr/th[contains(text(), "' + name +'")]/../td/div/text()').getall()
        elif len(response.xpath('//table[@class="infobox vcard"]/tbody/tr/th[contains(text(), "' + name +'")]/../td/div/*/text()').getall()) > 0:
            return response.xpath('//table[@class="infobox vcard"]/tbody/tr/th[contains(text(), "' + name +'")]/../td/div/*/text()').getall()
        elif len(response.xpath('//table[@class="infobox vcard"]/tbody/tr/th[contains(text(), "' + name +'")]/../td/div/*/a/text()').getall()) > 0:
            return response.xpath('//table[@class="infobox vcard"]/tbody/tr/th[contains(text(), "' + name +'")]/../td/div/*/a/text()').getall()
        elif len(response.xpath('//table[@class="infobox vcard"]/tbody/tr/th[contains(text(), "' + name +'")]/../td/text()').getall()) > 0:
            return response.xpath('//table[@class="infobox vcard"]/tbody/tr/th[contains(text(), "' + name +'")]/../td/text()').getall()
        else:
            return response.xpath('//table[@class="infobox vcard"]/tbody/tr/th[contains(text(), "' + name + '")]/../td//text()').getall()

