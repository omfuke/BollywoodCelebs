import scrapy
from ..items import CrawlcelebItem
import re


class Celebs(scrapy.Spider):

    name = 'newceleb'
    url = 'https://www.imdb.com/list/ls073889754/'

    def start_requests(self):
        yield scrapy.Request(url=self.url , callback= self.parse)


    def parse(self, response):
        links = response.css('.lister-item-header a::attr(href)').getall()

        #Following Links of celebs IMDB Recursively
        for link in links:
            yield response.follow(url = link , callback=self.parse_link)

        next_page = response.css('.next-page::attr(href)').get()

        #This is for next Page
        if next_page is not None:

            yield response.follow(url=next_page, callback= self.parse)

    def parse_link(self,response):

        name  = response.css('.header .itemprop::text').get()                   #Celebs Name
        DOB = response.css('#name-born-info time::attr(datetime)').get()
        try:
            producer = response.css('#filmo-head-producer::text').extract()[-1].lstrip(' ').replace('\n','')
            producer = int(re.search(r'\d+', producer).group())
        except:
            producer = 0

        try:

            director = response.css('#filmo-head-producer::text').extract()[-1].lstrip(' ').replace('\n','')
            director = int(re.search(r'\d+', director).group())
        except:
            director = 0

        try:
            music = response.css('#filmo-head-music_department::text').extract()[-1].lstrip(' ').replace('\n','')
            music = int(re.search(r'\d+', music).group())
        except:

            music = 0
        try:
            credits = response.css('#filmo-head-actor::text').extract()[-1].lstrip(' ').replace('\n','')
            credits = int(re.search(r'\d+', credits).group())
        except:
            credits = response.css('#filmo-head-actress::text').extract()[-1].lstrip(' ').replace('\n','')
            credits = int(re.search(r'\d+', credits).group())

        image = response.css('#name-poster::attr(src)').get()



        try:
            yield response.follow(url=response.css('#details-official-sites .inline a::attr(href)').get(),meta={'name':name,'producer':producer,'director':director,'music':music,'DOB':DOB,'credits':credits,'image':image},callback=self.parse_next)
        except:
            social = response.css('#details-official-sites a::text').getall()
            if len(social) == 0:
                social = 'null'




        yield {'name':name,'producer':producer,'director':director,'music':music,'DOB':DOB,'credits':credits,'social':social,'image':image}


    def parse_next(self,response):
        items = CrawlcelebItem()

        items['name'] = response.meta['name']
        items['producer'] = response.meta['producer']
        items['director'] = response.meta['director']
        items['music'] = response.meta['music']
        items['DOB'] = response.meta['DOB']
        items['credits'] = response.meta['credits']
        items['image'] = response.meta['image']
        items['social'] = ','.join(response.css('.simpleList:nth-child(4) a::text').getall())




        yield items