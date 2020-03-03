# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
df = pd.read_csv('/Users/ArkSealand/FIDS/Capstone/Scrapy/overbuff/overbuff/spiders/tagnames.csv')
iter_list = ['BluePillow-21338', 'Morellio-1416']
# print(iter_list)
class HeroesSpiderSpider(scrapy.Spider):
    name = 'heroes_spider'
    allowed_domains = ['www.overbuff.com']
    for name in iter_list:
        start_urls = ['https://www.overbuff.com/players/pc/'+str(name)]

        def parse(self, response):
            name = response.xpath("//div[@class='name']/a[@class='color-white']/text()").get()
            yield {
                'Hero': name
            }


