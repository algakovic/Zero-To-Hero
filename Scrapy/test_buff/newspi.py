# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
df = pd.read_csv('/Users/ArkSealand/FIDS/Capstone/Scrapy/overbuff/overbuff/spiders/tagnames.csv')
iter_list = ['Morellio-1416', 'BluePillow-21338']

class NewspiSpider(scrapy.Spider):
    name = 'newspi'
    allowed_domains = ['www.overbuff.com']
    start_urls = ['https://www.overbuff.com/players/pc/'+str(i) for i in iter_list]

    def parse(self, response):
        name = response.xpath("//div[@class='name']/a[@class='color-white']/text()").get()
        yield {
            'Hero': name
        }
