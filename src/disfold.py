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
    time_init = Field()
    time_finish = Field()
    time_search = Field()
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
         item["time_init"] = time.time()
         item["name"] = self.auxiliary('name',row) 
         item["market_cap"] = self.auxiliary('market_cap',row)                                
         item["stock"] = self.auxiliary('stock',row)                                          
         item["country"] = self.auxiliary('country',row)                                       
         item["sector"] =  self.auxiliary('sector',row)                                        
         item["industry"] = self.auxiliary('industry',row)
         item["time_search"] = time.time()- item["time_init"]                                     
            
         href = row.xpath("td[2]/a/@href").get()
         yield scrapy.Request(response.urljoin(href), self.parse2, cb_kwargs=dict(item = item))


   

   
         
   def parse2(self, response, item):
      item['headquarters'] = ""
      item['founded'] = ""
      item['employees'] = ""
      item['ceo'] = ""
      time_init2 = time.time()
      
      
      if (response.xpath("//*[@class = 'card-content cyan darken-4']/p[2]/text()") != []):
         elem = response.xpath("//*[@class = 'card-content cyan darken-4']/p[2]/text()").get()
         if(elem.find("Headquarters") != -1):
            item['headquarters'] = elem.replace(" ","").replace("Headquarters:", "").replace("\n", "")
         elif(elem.find("Founded") != -1):
            item['founded'] = elem.replace("Founded:", "").replace("\n", "")
         elif(elem.find("Employees") != -1):
            item['employees'] = elem.replace("Employees:", "").replace("\n", "")
         elif(elem.find("CEO") != -1):
            item['ceo'] = elem.replace("CEO:", "").replace("\n", "")

      if (response.xpath("//*[@class = 'card-content cyan darken-4']/p[3]/text()") != []):
         elem = response.xpath("//*[@class = 'card-content cyan darken-4']/p[3]/text()").get()
         if(elem.find("Headquarters") != -1):
            item['headquarters'] = elem.replace(" ","").replace("Headquarters:", "").replace("\n", "")
         elif(elem.find("Founded") != -1):
            item['founded'] = elem.replace("Founded:", "").replace("\n", "")
         elif(elem.find("Employees") != -1):
            item['employees'] = elem.replace("Employees:", "").replace("\n", "")
         elif(elem.find("CEO") != -1):
            item['ceo'] = elem.replace("CEO:", "").replace("\n", "")

    
      if (response.xpath("//*[@class = 'card-content cyan darken-4']/p[4]/text()") != []):
         elem = response.xpath("//*[@class = 'card-content cyan darken-4']/p[4]/text()").get()
         if(elem.find("Headquarters") != -1):
            item['headquarters'] = elem.replace(" ","").replace("Headquarters:", "").replace("\n", "")
         elif(elem.find("Founded") != -1):
            item['founded'] = elem.replace("Founded:", "").replace("\n", "")
         elif(elem.find("Employees") != -1):
            item['employees'] = elem.replace("Employees:", "").replace("\n", "")
         elif(elem.find("CEO") != -1):
            item['ceo'] = elem.replace("CEO:", "").replace("\n", "")
            
      
     
      if (response.xpath("//*[@class = 'card-content cyan darken-4']/p[5]/text()") != []):
         elem = response.xpath("//*[@class = 'card-content cyan darken-4']/p[5]/text()").get()
         if(elem.find("Headquarters") != -1):
            item['headquarters'] = elem.replace(" ","").replace("Headquarters:", "").replace("\n", "")
         elif(elem.find("Founded") != -1):
            item['founded'] = elem.replace("Founded:", "").replace("\n", "")
         elif(elem.find("Employees") != -1):
            item['employees'] = elem.replace("Employees:", "").replace("\n", "")
         elif(elem.find("CEO") != -1):
            item['ceo'] = elem.replace("CEO:", "").replace("\n", "")
      

      
      if (response.xpath("//*[@class = 'card-content cyan darken-4']/p[6]/text()") != []):
         elem = response.xpath("//*[@class = 'card-content cyan darken-4']/p[6]/text()").get()
         if(elem.find("Headquarters") != -1):
            item['headquarters'] = elem.replace(" ","").replace("Headquarters:", "")
         elif(elem.find("Founded") != -1):
            item['founded'] = elem.replace("Founded:", "").replace("\n", "")
         elif(elem.find("Employees") != -1):
            item['employees'] = elem.replace("Employees:", "").replace("\n", "")
         elif(elem.find("CEO") != -1):
            item['ceo'] = elem.replace("CEO:", "").replace("\n", "")
      

      item["time_finish"] = time.time()
      item["time_search"] = item["time_search"]+ time.time()-time_init2 

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


        

