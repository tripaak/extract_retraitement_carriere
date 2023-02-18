# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import joblib
from extract_historique import dict_of_version
dict_of_version=joblib.load("fifa20\\spiders\\date.pkl")

def convert_saison(an):
    if '/' not in an:
        an=''.join([str(int(an)),'/',str(int(an)+1)])
    return an

class SelectionsSpider(scrapy.Spider):
    name = 'selections'
    allowed_domains = ['sofifa.com']
    start_urls = ['https://sofifa.com/players?col=oa&sort=desc&showCol%5B0%5D=pi&showCol%5B1%5D=ae&showCol%5B2%5D=hi&showCol%5B3%5D=wi&showCol%5B4%5D=pf&showCol%5B5%5D=oa&showCol%5B6%5D=pt&showCol%5B7%5D=bo&showCol%5B8%5D=bp&showCol%5B9%5D=gu&showCol%5B10%5D=jt&showCol%5B11%5D=le&showCol%5B12%5D=vl&showCol%5B13%5D=wg&showCol%5B14%5D=rc&showCol%5B15%5D=ta&showCol%5B16%5D=cr&showCol%5B17%5D=fi&showCol%5B18%5D=he&showCol%5B19%5D=sh&showCol%5B20%5D=vo&showCol%5B21%5D=ts&showCol%5B22%5D=dr&showCol%5B23%5D=cu&showCol%5B24%5D=fr&showCol%5B25%5D=lo&showCol%5B26%5D=bl&showCol%5B27%5D=to&showCol%5B28%5D=ac&showCol%5B29%5D=sp&showCol%5B30%5D=ag&showCol%5B31%5D=re&showCol%5B32%5D=ba&showCol%5B33%5D=tp&showCol%5B34%5D=so&showCol%5B35%5D=ju&showCol%5B36%5D=st&showCol%5B37%5D=sr&showCol%5B38%5D=ln&showCol%5B39%5D=te&showCol%5B40%5D=ar&showCol%5B41%5D=in&showCol%5B42%5D=po&showCol%5B43%5D=vi&showCol%5B44%5D=pe&showCol%5B45%5D=cm&showCol%5B46%5D=td&showCol%5B47%5D=ma&showCol%5B48%5D=sa&showCol%5B49%5D=sl&showCol%5B50%5D=tg&showCol%5B51%5D=gd&showCol%5B52%5D=gh&showCol%5B53%5D=gk&showCol%5B54%5D=gp&showCol%5B55%5D=gr&showCol%5B56%5D=tt&showCol%5B57%5D=bs&showCol%5B58%5D=wk&showCol%5B59%5D=sk&showCol%5B60%5D=aw&showCol%5B61%5D=dw&showCol%5B62%5D=ir&showCol%5B63%5D=pac&showCol%5B64%5D=sho&showCol%5B65%5D=pas&showCol%5B66%5D=dri&showCol%5B67%5D=def&showCol%5B68%5D=phy&r={}&set=true'.format(dict_of_version['key'])]
    def parse(self, response):
        #headers = response.css('table.table>thead>tr>th ::text').extract()[5:]
        for player in response.css('table.table>tbody>tr'):
            #for player in response.css('body > div.center > div > div.col.col-12 > div:nth-child(6) > table > tbody > tr'):
            item = {}
            Name = player.css('td.col-name>a::attr(aria-label)').extract()
            page_ref = player.css('td.col-name>a::attr(href)').get()
            ID= player.css('td.col.col-pi::text').get()  
            lien_selection = Request(url="https://sofifa.com/player/"+str(ID)+"/live",callback=self.parse_selection,meta={'id':ID,'Name':Name})
            yield lien_selection
        next_page = response.xpath('//span[@class="bp3-button-text" and text()="Next"]/parent::a/@href').get()

        if next_page:
            yield Request(response.urljoin(next_page))

 

    def parse_date(self, response):
        item = response.meta['item']
        date = response.xpath('//*[@id="body"]/div[2]/div/div[2]/div[1]/div/div/text()').extract()[-1]
        item["birth"] = date.split("(")[1].split(")")[0]
        return item

    def parse_selection(self, response):
        #headers= response.css()
         ID= response.meta['id']
         Name=response.meta['Name']
         center = response.css('body > div.center > div > div.col.col-12')
         for i in range(1,8):                              #méthode de boucle identique à celle de  parse_transferts
                transfers =  center.css(f'div:nth-child({i})>h5').extract()
                print(transfers)
                if len(transfers)==1:
                    if "National Team" in transfers[0]:
                        for ltr in center.css('div:nth-child({}) > table > tbody>tr'.format(i)):
                            item ={}
                            item['ID_Player']=ID
                            item['Name']=Name
                            item ['birth_date']=ltr.xpath('//*[@id="body"]/div[1]/div/div[1]/div[1]/ul[1]/li[2]/text()').extract()
                            item["Saison"]=ltr.xpath('td[1]/text()').extract()
                            item['Team']=ltr.xpath('td[2]/a/text()').extract()
                            if len(item["Team"])==0:
                                    item["Team"]=ltr.xpath('td[2]/text()').extract()      
                            item["Competition"]=ltr.xpath('td[3]/text()').extract()
                            item["Minutes_Jouées"]=ltr.xpath('td[4]/text()').extract()
                            item["Apparition"]=ltr.xpath('td[5]/text()').extract() 
                            item["Titulaire"]=ltr.xpath('td[6]/text()').extract()     
                            item["Remplacé_xfois"]=ltr.xpath('td[7]/text()').extract()     
                            item["A Remplacé_xfois"]=ltr.xpath('td[8]/text()').extract()     
                            item["Sur le banc"]=ltr.xpath('td[9]/text()').extract() 
                            item["Saison_trait"]=convert_saison(item["Saison"][0])              
                            yield item
