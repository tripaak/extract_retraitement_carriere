# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import scrapy
from scrapy import Request
import joblib
from extract_historique import dict_of_version
dict_of_version=joblib.load("fifa20\\spiders\\date.pkl")
class TeamsSpider(scrapy.Spider):
    name = 'equipes'
    allowed_domains = ['sofifa.com']
    start_urls = ['https://sofifa.com/teams?r={}&set=true'.format(dict_of_version['key'])]
    
    def parse(self, response):                 #fonction de scrapping de l'url attribué à "start_urls"
        #headers = response.css('table.table>thead>tr>th ::text').extract()[5:]  #permet de récupérer le nom des colonnes souhaitées
        for player in response.xpath('//*[@id="body"]/div[1]/div/div[2]/div/table/tbody/tr'): #pour toute les lignes du tableau correspondant 
            item={}

            item['Update_Date_Team']=player.xpath('//*[@id="body"]/header/div[2]/div/h2/div[2]/a/span[1]/text()').extract()[0]#.replace('"','')    #on attribue à la colonne la valeur correspondante
            item['Competition_ID']=player.css('tr> td.col-name-wide > a.sub::attr(href)').extract()[0].split('=')[1]
            item['Competiton']=player.css(' tr > td.col-name-wide > a.sub > div ::text').extract()[0].split("(")[0]
            #item['Rang_Comp']=player.css('tr > td.col-name-wide > a.sub > div ::text').extract()[0].split("(")[1].split(")")[0](pas présent pour toutes les équipes)
            item['Team_ID']=player.css('td.col-name-wide > a:nth-child(1)::attr(href)').extract()[0].split("/")[2]
            item['Team']=player.css('a:nth-child(1) > div::text').extract()
            print(item['Team'])
            item['Overall_Comp']=player.css('tr> td.col.col-oa> span::text').extract()
            item['Attack_Comp']=player.css('tr> td.col.col-at > span::text').extract()
            item['Milieu_Comp']=player.css('tr> td.col.col-md > span::text').extract()
            item['Defense_Comp']=player.css(' tr> td.col.col-df >span::text ').extract()
            item['NbJoueurs_Team']=player.css('tr> td.col.col-ps::text').extract()
            lien_pays=Request(url="https://sofifa.com/team/"+item['Team_ID'],callback=self.parse_pays,meta={'item':item})
            yield lien_pays  #permet de retourner les éléments scrappés
            
        next_page = response.xpath('//span[@class="bp3-button-text" and text()="Next"]/parent::a/@href').get()

        if next_page:
            yield Request(response.urljoin(next_page))
    
    def parse_pays(self,response):
        item=response.meta['item']
        item['pays']=response.css('div.info > div > a:nth-child(1)::attr(title)').get()
        yield item