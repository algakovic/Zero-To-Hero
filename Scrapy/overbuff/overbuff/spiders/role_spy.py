# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
df = pd.read_csv('/Users/ArkSealand/FIDS/Capstone/Scrapy/overbuff/overbuff/spiders/tagnames.csv')
iter_list = df['Battle_Tag'].tolist()
class NewspiSpider(scrapy.Spider):
    name = 'role_spy'
    allowed_domains = ['www.overbuff.com']
    
    
    start_urls = ['https://www.overbuff.com/players/pc/'+str(i) for i in iter_list]
    

    def parse(self, response):
        total_wins = response.xpath("//dd/span[@class='color-stat-win']/text()").get()

        # role1 = response.xpath("//div[@data-portable='roles']/section/article/table/tbody/tr/td/@data-value[not(. < //div[@data-portable='roles']/section/article/table/tbody/tr/td[@data-value])][0]/parent::td/parent::tr[0]/td/a[@class='color-white']/text()").get()
        # wins1 = response.xpath("//div[@data-portable='roles']/section/article/table/tbody/tr/td/@data-value[not(. < //div[@data-portable='roles']/section/article/table/tbody/tr/td[@data-value])]")[1].get()
        # role2 = response.xpath("//div[@data-portable='roles']/section/article/table/tbody/tr/td/@data-value[not(. < //div[@data-portable='roles']/section/article/table/tbody/tr/td[@data-value])][1]/parent::td/parent::tr[1]/td/a[@class='color-white']/text()").get()
        # wins2 = response.xpath("//div[@data-portable='roles']/section/article/table/tbody/tr/td/@data-value[not(. < //div[@data-portable='roles']/section/article/table/tbody/tr/td[@data-value])]")[2].get()

        information = response.xpath("//div[@data-portable='roles']/section/article/table/tbody/tr")
        # role_data_values = response.xpath("//div[@data-portable='roles']/section/article/table/tbody/tr/td/@data-value/text()").getall()
        new_dict = {'Battle_Tag': response.xpath("//div[@class='layout-header-primary-bio']/h1/text()").get()+response.xpath("//div[@class='layout-header-primary-bio']/h1/small/text()").get().replace('#', '-'),
                    'Total_Wins': total_wins}
        for i in range(len(information)):
            new_dict[f'Top_role_'+str(i)] = information.xpath(".//td/a[@class='color-white']/text()")[i].get()
            new_dict[f'role_wins_'+str(i)] = information.xpath(".//td/@data-value")[i].get()
        return new_dict