import scrapy
from scrapy.item import Item, Field
import time 


class CustomItem(Item):
    name = Field()
    market_cap = Field()
    stock = Field()
    country = Field()
    sector = Field()
    industry = Field()
    headquarters = Field() 
    founded = Field()
    employees = Field()
    ceo = Field()
    #time_init = Field()
    #time_finish = Field()
    #time_search = Field()
    #description = Field() 


class DisfoldSpider(scrapy.Spider):
   name = 'disfold'
   allowed_domains = ['disfold.com']
   start_urls = ['https://disfold.com/world/companies/']
   next_page = "?page=1"

   def parse(self, response):
      i = 1 
      while(i!= 21):
         url = self.start_urls[0] +"?page="+ str(i)
         #self.next_page = response.xpath("//div[@class='pagination']/ul/..//li[last()-1]/a/@href").get()
         #self.logger.info(self.current)
         #self.logger.info(self.next_page)
         #if self.next_page is not None:
         yield response.follow(url, callback = self.f)
         i = i+1


   def f(self,response):
      for row in response.xpath('//descendant-or-self::table/tbody/tr'): 
         item = CustomItem()
         #item["time_init"] = time.time()
         item["name"] = self.auxiliary('name',row) 
         item["market_cap"] = self.auxiliary('market_cap',row)                                
         item["stock"] = self.auxiliary('stock',row)                                          
         item["country"] = self.auxiliary('country',row)                                       
         item["sector"] =  self.auxiliary('sector',row)                                        
         item["industry"] = self.auxiliary('industry',row)                                     
            
         href = row.xpath("td[2]/a/@href").get()
         yield scrapy.Request(response.urljoin(href), self.parse2, cb_kwargs=dict(item = item))


   

   
         
   def parse2(self, response, item):
      item['headquarters'] = ""
      item['founded'] = ""
      item['employees'] = ""
      item['ceo'] = ""
      
      elem = response.xpath("//*[@class = 'card-content cyan darken-4']/p[3]/text()")
      if (elem != []):
         if(elem.get().find("Headquarters") == 0):
            item['headquarters'] = elem.get().replace(" ","").replace("Headquarters:", "").replace("\n", "")
         elif(elem.get().find("Founded") == 0):
            item['founded'] = elem.get().replace("Founded:", "").replace("\n", "").strip()
         elif(elem.get().find("Employees") == 0):
            item['employees'] = elem.get().replace("Employees:", "").replace("\n", "").strip()
         elif(elem.get().find("CEO") == 0):
            item['ceo'] = elem.get().replace("CEO:", "").replace("\n", "").strip()

      elem = response.xpath("//*[@class = 'card-content cyan darken-4']/p[4]/text()")
      if (elem != []):
         if(elem.get().find("Headquarters") == 0):
            item['headquarters'] = elem.get().replace(" ","").replace("Headquarters:", "").replace("\n", "").strip()
         elif(elem.get().find("Founded") == 0):
            item['founded'] = elem.get().replace("Founded:", "").replace("\n", "").strip()
         elif(elem.get().find("Employees") == 0):
            item['employees'] = elem.get().replace("Employees:", "").replace("\n", "").strip()
         elif(elem.get().find("CEO") == 0):
            item['ceo'] = elem.get().replace("CEO:", "").replace("\n", "").strip()
            
      
      elem = response.xpath("//*[@class = 'card-content cyan darken-4']/p[5]/text()")
      if (elem != []):
         if(elem.get().find("Headquarters") == 0):
            item['headquarters'] = elem.get().replace(" ","").replace("Headquarters:", "").replace("\n", "").strip()
         elif(elem.get().find("Founded") == 0):
            item['founded'] = elem.get().replace("Founded:", "").replace("\n", "").strip()
         elif(elem.get().find("Employees") == 0):
            item['employees'] = elem.get().replace("Employees:", "").replace("\n", "").strip()
         elif(elem.get().find("CEO") == 0):
            item['ceo'] = elem.get().replace("CEO:", "").replace("\n", "").strip()
      

      elem = response.xpath("//*[@class = 'card-content cyan darken-4']/p[6]/text()")
      if (elem != []):
         if(elem.get().find("Headquarters") == 0):
            item['headquarters'] = elem.get().replace(" ","").replace("Headquarters:", "").replace("\n", "")
         elif(elem.get().find("Founded") == 0):
            item['founded'] = elem.get().replace("Founded:", "").replace("\n", "")
         elif(elem.get().find("Employees") == 0):
            item['employees'] = elem.get().replace("Employees:", "").replace("\n", "")
         elif(elem.get().find("CEO") == 0):
            item['ceo'] = elem.get().replace("CEO:", "").replace("\n", "")
      

      #item["time_finish"] = time.time()
      #item["time_search"] = item["time_finish"]-item["time_init"]

      return item

 
   def auxiliary(self,value,row):
      match value:
         case 'name':
            if(row.xpath('td[2]/a/text()') != []):
               return row.xpath('td[2]/a/text()').get().strip().replace("\n","")
            elif(row.xpath('td[3]/text()') != []):
               return row.xpath('td[3]/text()').get().strip().replace("\n","")
            else:
               return ""
         case 'market_cap':
            if(row.xpath('td[3]/a/text()') != []):
               return row.xpath('td[3]/a/text()').get().strip().replace("\n","")
            elif(row.xpath('td[3]/text()') != []):
               return row.xpath('td[3]/text()').get().strip().replace("\n","")
            else:
               return ""
         case 'stock':
            if(row.xpath('td[4]/a/text()') != []):
               return row.xpath('td[4]/a/text()').get().strip().replace("\n","")
            elif(row.xpath('td[4]/text()') != []):
               return row.xpath('td[4]/text()').get().strip().replace("\n","")
            else:
               return ""
         case 'country':
            if(row.xpath('td[5]/a/text()[2]') != []):
               return row.xpath('td[5]/a/text()[2]').get().strip().replace("\n","")
            elif(row.xpath('td[5]/a/text()') != []):
               return row.xpath('td[5]/a/text()').get().strip().replace("\n","")
            elif(row.xpath('td[5]/text()[2]') != [] ):
               return row.xpath('td[5]/text()[2]').get().strip().replace("\n","")
            elif(row.xpath('td[5]/text()') != []):
               return row.xpath('td[5]/text()').get().strip().replace("\n","")
            else:
               return ""
         case 'sector':
            if(row.xpath('td[6]/a/text()[2]') != [] ):
               return row.xpath('td[6]/a/text()[2]').get().replace("\n","")
            elif(row.xpath('td[6]/a/text()') != []):
               return row.xpath('td[6]/a/text()').get().replace("\n","")
            elif(row.xpath('td[6]/text()') != []  ):
               return row.xpath('td[6]/text()').get().replace("\n","")
            elif(row.xpath('td[6]/text()[2]') != [] ):
               return row.xpath('td[6]/text()[2]').get().replace("\n","")
            else:
               return ""
         case 'industry':
            if(row.xpath('td[7]/a/text()[2]') != [] ):
               return row.xpath('td[7]/a/text()[2]').get().replace("\n","")
            elif(row.xpath('td[7]/a/text()') != [] ):
               return row.xpath('td[7]/a/text()').get().replace("\n","")
            elif(row.xpath('td[7]/text()[2]') != [] ):
               return row.xpath('td[7]/text()[2]').get().replace("\n","")
            elif(row.xpath('td[7]/text()') != [] ):
               return row.xpath('td[7]/text()').get().replace("\n","")
            else:
               return ""


        

