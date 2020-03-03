# -*- coding: utf-8 -*-
import scrapy
import logging

class BattletagsSpider(scrapy.Spider):
    name = 'battletags'
    allowed_domains = ['overwatchtracker.com']
    start_urls = [f'https://overwatchtracker.com/leaderboards/pc/global/CompetitiveRank?page={i}' for i in range(1,3989)]

    def parse(self, response):
        players = response.xpath("//td/a[starts-with(@href, '/profile')]")
        for player in players:
            battletag_id = player.xpath(".//text()").get()
            link = player.xpath(".//@href").get()

            absolute_url = f"https://www.overwatchtracker.com/{link}"
            yield scrapy.Request(url = absolute_url, callback=self.parse_player, meta={'tag_name':battletag_id})
        
        
        

    def parse_player(self, response):
        battletagid = response.request.meta['tag_name']
        stats_values = response.xpath("//div[@class='value']/text()").getall()
        stats_names = response.xpath("//div[@class='name']/text()").getall()
        new_dict = {'Battle_Tag': battletagid}
        for i in range(len(stats_values)):
            if stats_values[i]:
                new_dict[stats_names[i].strip()] = stats_values[i].strip()
            else: new_dict[stats_names[i]] = 'error'
        return new_dict
        

        
        # yield {
        #     'Battle_Tag': battletagid,
        #     'Level': stats_values[0].strip(),
        #     'Skill Rating': stats_values[1].strip(),
        #     'K/d Ratio': stats_values[2].strip(),
        #     'Ka/d Ratio': stats_values[3].strip(),
        #     'Win %': stats_values[4].strip(),
        #     'Kills per Game': stats_values[5].strip(),
        #     'Eliminations per Game': stats_values[6].strip(),
        #     'Damage per Game': stats_values[7].strip(),
        #     'Healing per Game': stats_values[8].strip(),
        #     'Eliminations per Min': stats_values[9].strip(),
        #     'Healing per Min': stats_values[10].strip(),
        #     'Damage per Min': stats_values[11].strip(),
        #     'Solo Kills': stats_values[12].strip(),
        #     'Objective Kills': stats_values[13].strip(),
        #     'Final Blows': stats_values[14].strip(),
        #     'Damage Done': stats_values[15].strip(),
        #     'Eliminations': stats_values[16].strip(),
        #     'Environmental Kills': stats_values[17].strip(),
        #     'Multi Kills': stats_values[18].strip(),
        #     'Deaths': stats_values[19].strip(),
        #     'Environmental Deaths': stats_values[20].strip(),
        #     'Games Won': stats_values[21].strip(),
        #     'Games Played': stats_values[22].strip(),
        #     'Time Spent On Fire': stats_values[23].strip(),
        #     'Objective Time': stats_values[24].strip(),
        #     'Time Played': stats_values[25].strip(),
        #     'Assists': stats_values[26].strip(),
        #     'Healing Done': stats_values[27].strip(),
        #     'Defensive Assists': stats_values[28].strip(),
        #     'Offensive Assists': stats_values[29].strip(),
        #     'Most Eliminations': stats_values[30].strip(),
        #     'Most Final Blows': stats_values[31].strip(),
        #     'Most Damage Done': stats_values[32].strip(),
        #     'Most Healing': stats_values[33].strip(),
        #     'Most Defensive Assists': stats_values[34].strip(),
        #     'Most Offensive Assists': stats_values[35].strip(),
        #     'Most Objective Kills': stats_values[36].strip(),
        #     'Most Objective Time': stats_values[37].strip(),
        #     'Most Solo Kills': stats_values[38].strip(),
        #     'Most Time Spent On Fire': stats_values[39].strip(),
        #     }


        # profile_link = response.request.meta['profile_link']
        # logging.info(response.url)
        # top_hero_link = response.xpath("//div[@class = 'material-card hero'][1]/div/h2/a/@href").get()

        # absolute_url = f"{profile_link}/{top_hero_link}"
        # yield scrapy.Request(url = absolute_url)

