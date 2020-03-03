# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
df = pd.read_csv('/Users/ArkSealand/FIDS/Capstone/Scrapy/overwatch/200kTags.csv')
iter_list = df['Battle_Tag'].tolist()
class NewspiSpider(scrapy.Spider):
    name = 'hero_name'
    allowed_domains = ['www.overbuff.com']
    
    
    start_urls = ['https://www.overbuff.com/players/pc/'+str(i) for i in iter_list]
    

    def parse(self, response):
        info = response.xpath("//div[@class='name']/a[@class='color-white']/text()").getall()
        # name1 = response.xpath("//div[@class='name']/a[@class='color-white']/text()")[0].get()
        # name2 = response.xpath("//div[@class='name']/a[@class='color-white']/text()")[1].get()
        # name3 = response.xpath("//div[@class='name']/a[@class='color-white']/text()")[2].get()
        # name4 = response.xpath("//div[@class='name']/a[@class='color-white']/text()")[3].get()
        # name5 = response.xpath("//div[@class='name']/a[@class='color-white']/text()")[4].get()
        idpath = response.xpath("//div[@class='layout-header-primary-bio']/h1/text()").get()+response.xpath("//div[@class='layout-header-primary-bio']/h1/small/text()").get().replace('#', '-')
        new_dict = {'Battle_Tag': idpath}
        for i in range(len(info)):
            if i == 5:
                break
            new_dict['Hero'+str(i+1)]= info[i]
                # 'Hero1': name1,
                # 'Hero2': name2,
                # 'Hero3': name3,
                # 'Hero4': name4,
        #         'Hero5': name5
        # }
        return new_dict