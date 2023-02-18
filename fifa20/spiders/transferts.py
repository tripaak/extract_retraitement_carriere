# -*- coding: utf-8 -*-
import scrapy
import numpy as np
from scrapy import Request
from datetime import datetime
import joblib
from extract_historique import dict_of_version
dict_of_version=joblib.load("fifa20\\spiders\\date.pkl")

def comp_date(date_string_1): #fonction permetant de créer la saison correspondante en fonction de la date
        date_object_1=datetime.strptime(date_string_1,"%b %d, %Y")
        date_string_2 = ("Jun 30, {}").format(date_object_1.year)
        date_object_2=datetime.strptime(date_string_2,"%b %d, %Y")
        print(date_object_2)
        if (date_object_1<date_object_2):
            return ''.join([str(date_object_2.year-1),"/",str(date_object_2.year)])
        else:
            return ''.join([str(date_object_2.year),"/",str(date_object_2.year+1)])

def convert_prix(val):      #fonction permettant de convertir au format int les valeurs de transferts
    monnaie={'€','$','£'}
    for i in monnaie:
        if i in val:
            val=val.split('{}'.format(i))[1]
            if 'K'in val:
                val=int(val.split('K')[0])/1000
                print(val)
            elif 'k'in val:
                val=int(val.split('K')[0])/1000
                print(val)    
            elif 'M' in val:
                     val=int(val.split('M')[0])
            return val

class SofifaSpider(scrapy.Spider):

    name = 'transferts'

    allowed_domains = ['sofifa.com']

    start_urls = ['https://sofifa.com/players?showCol%5B0%5D=pi&showCol%5B1%5D=ae&showCol%5B2%5D=hi&showCol%5B3%5D=wi&showCol%5B4%5D=pf&showCol%5B5%5D=oa&showCol%5B6%5D=pt&showCol%5B7%5D=bo&showCol%5B8%5D=bp&showCol%5B9%5D=gu&showCol%5B10%5D=jt&showCol%5B11%5D=le&showCol%5B12%5D=vl&showCol%5B13%5D=wg&showCol%5B14%5D=rc&showCol%5B15%5D=ta&showCol%5B16%5D=cr&showCol%5B17%5D=fi&showCol%5B18%5D=he&showCol%5B19%5D=sh&showCol%5B20%5D=vo&showCol%5B21%5D=ts&showCol%5B22%5D=dr&showCol%5B23%5D=cu&showCol%5B24%5D=fr&aeh=18&showCol%5B25%5D=lo&showCol%5B26%5D=bl&showCol%5B27%5D=to&showCol%5B28%5D=ac&showCol%5B29%5D=sp&showCol%5B30%5D=ag&showCol%5B31%5D=re&showCol%5B32%5D=ba&showCol%5B33%5D=tp&showCol%5B34%5D=so&showCol%5B35%5D=ju&showCol%5B36%5D=st&showCol%5B37%5D=sr&showCol%5B38%5D=ln&showCol%5B39%5D=te&showCol%5B40%5D=ar&showCol%5B41%5D=in&showCol%5B42%5D=po&showCol%5B43%5D=vi&showCol%5B44%5D=pe&showCol%5B45%5D=cm&showCol%5B46%5D=td&showCol%5B47%5D=ma&showCol%5B48%5D=sa&showCol%5B49%5D=sl&showCol%5B50%5D=tg&showCol%5B51%5D=gd&showCol%5B52%5D=gh&showCol%5B53%5D=gp&showCol%5B54%5D=gr&showCol%5B55%5D=tt&showCol%5B56%5D=bs&showCol%5B57%5D=wk&showCol%5B58%5D=sk&showCol%5B59%5D=aw&showCol%5B60%5D=dw&showCol%5B61%5D=ir&showCol%5B62%5D=pac&showCol%5B63%5D=sho&showCol%5B64%5D=pas&showCol%5B65%5D=dri&showCol%5B66%5D=def&showCol%5B67%5D=phy&showCol%5B68%5D=gc&r={}&set=true'.format(dict_of_version['key']),
            'https://sofifa.com/players?showCol%5B0%5D=pi&showCol%5B1%5D=ae&showCol%5B2%5D=hi&showCol%5B3%5D=wi&showCol%5B4%5D=pf&showCol%5B5%5D=oa&showCol%5B6%5D=pt&showCol%5B7%5D=bo&showCol%5B8%5D=bp&showCol%5B9%5D=gu&showCol%5B10%5D=jt&showCol%5B11%5D=le&showCol%5B12%5D=vl&showCol%5B13%5D=wg&showCol%5B14%5D=rc&showCol%5B15%5D=ta&showCol%5B16%5D=cr&showCol%5B17%5D=fi&showCol%5B18%5D=he&showCol%5B19%5D=sh&showCol%5B20%5D=vo&showCol%5B21%5D=ts&showCol%5B22%5D=dr&showCol%5B23%5D=cu&showCol%5B24%5D=fr&ael=19&aeh=21&showCol%5B25%5D=lo&showCol%5B26%5D=bl&showCol%5B27%5D=to&showCol%5B28%5D=ac&showCol%5B29%5D=sp&showCol%5B30%5D=ag&showCol%5B31%5D=re&showCol%5B32%5D=ba&showCol%5B33%5D=tp&showCol%5B34%5D=so&showCol%5B35%5D=ju&showCol%5B36%5D=st&showCol%5B37%5D=sr&showCol%5B38%5D=ln&showCol%5B39%5D=te&showCol%5B40%5D=ar&showCol%5B41%5D=in&showCol%5B42%5D=po&showCol%5B43%5D=vi&showCol%5B44%5D=pe&showCol%5B45%5D=cm&showCol%5B46%5D=td&showCol%5B47%5D=ma&showCol%5B48%5D=sa&showCol%5B49%5D=sl&showCol%5B50%5D=tg&showCol%5B51%5D=gd&showCol%5B52%5D=gh&showCol%5B53%5D=gp&showCol%5B54%5D=gr&showCol%5B55%5D=tt&showCol%5B56%5D=bs&showCol%5B57%5D=wk&showCol%5B58%5D=sk&showCol%5B59%5D=aw&showCol%5B60%5D=dw&showCol%5B61%5D=ir&showCol%5B62%5D=pac&showCol%5B63%5D=sho&showCol%5B64%5D=pas&showCol%5B65%5D=dri&showCol%5B66%5D=def&showCol%5B67%5D=phy&showCol%5B68%5D=gc&r={}&set=true'.format(dict_of_version['key']),
            'https://sofifa.com/players?showCol%5B0%5D=pi&showCol%5B1%5D=ae&showCol%5B2%5D=hi&showCol%5B3%5D=wi&showCol%5B4%5D=pf&showCol%5B5%5D=oa&showCol%5B6%5D=pt&showCol%5B7%5D=bo&showCol%5B8%5D=bp&showCol%5B9%5D=gu&showCol%5B10%5D=jt&showCol%5B11%5D=le&showCol%5B12%5D=vl&showCol%5B13%5D=wg&showCol%5B14%5D=rc&showCol%5B15%5D=ta&showCol%5B16%5D=cr&showCol%5B17%5D=fi&showCol%5B18%5D=he&showCol%5B19%5D=sh&showCol%5B20%5D=vo&showCol%5B21%5D=ts&showCol%5B22%5D=dr&showCol%5B23%5D=cu&showCol%5B24%5D=fr&ael=22&aeh=27&showCol%5B25%5D=lo&showCol%5B26%5D=bl&showCol%5B27%5D=to&showCol%5B28%5D=ac&showCol%5B29%5D=sp&showCol%5B30%5D=ag&showCol%5B31%5D=re&showCol%5B32%5D=ba&showCol%5B33%5D=tp&showCol%5B34%5D=so&showCol%5B35%5D=ju&showCol%5B36%5D=st&showCol%5B37%5D=sr&showCol%5B38%5D=ln&showCol%5B39%5D=te&showCol%5B40%5D=ar&showCol%5B41%5D=in&showCol%5B42%5D=po&showCol%5B43%5D=vi&showCol%5B44%5D=pe&showCol%5B45%5D=cm&showCol%5B46%5D=td&showCol%5B47%5D=ma&showCol%5B48%5D=sa&showCol%5B49%5D=sl&showCol%5B50%5D=tg&showCol%5B51%5D=gd&showCol%5B52%5D=gh&showCol%5B53%5D=gp&showCol%5B54%5D=gr&showCol%5B55%5D=tt&showCol%5B56%5D=bs&showCol%5B57%5D=wk&showCol%5B58%5D=sk&showCol%5B59%5D=aw&showCol%5B60%5D=dw&showCol%5B61%5D=ir&showCol%5B62%5D=pac&showCol%5B63%5D=sho&showCol%5B64%5D=pas&showCol%5B65%5D=dri&showCol%5B66%5D=def&showCol%5B67%5D=phy&showCol%5B68%5D=gc&r={}&set=true'.format(dict_of_version['key']),
            'https://sofifa.com/players?showCol%5B0%5D=pi&showCol%5B1%5D=ae&showCol%5B2%5D=hi&showCol%5B3%5D=wi&showCol%5B4%5D=pf&showCol%5B5%5D=oa&showCol%5B6%5D=pt&showCol%5B7%5D=bo&showCol%5B8%5D=bp&showCol%5B9%5D=gu&showCol%5B10%5D=jt&showCol%5B11%5D=le&showCol%5B12%5D=vl&showCol%5B13%5D=wg&showCol%5B14%5D=rc&showCol%5B15%5D=ta&showCol%5B16%5D=cr&showCol%5B17%5D=fi&showCol%5B18%5D=he&showCol%5B19%5D=sh&showCol%5B20%5D=vo&showCol%5B21%5D=ts&showCol%5B22%5D=dr&showCol%5B23%5D=cu&showCol%5B24%5D=fr&ael=25&aeh=28&showCol%5B25%5D=lo&showCol%5B26%5D=bl&showCol%5B27%5D=to&showCol%5B28%5D=ac&showCol%5B29%5D=sp&showCol%5B30%5D=ag&showCol%5B31%5D=re&showCol%5B32%5D=ba&showCol%5B33%5D=tp&showCol%5B34%5D=so&showCol%5B35%5D=ju&showCol%5B36%5D=st&showCol%5B37%5D=sr&showCol%5B38%5D=ln&showCol%5B39%5D=te&showCol%5B40%5D=ar&showCol%5B41%5D=in&showCol%5B42%5D=po&showCol%5B43%5D=vi&showCol%5B44%5D=pe&showCol%5B45%5D=cm&showCol%5B46%5D=td&showCol%5B47%5D=ma&showCol%5B48%5D=sa&showCol%5B49%5D=sl&showCol%5B50%5D=tg&showCol%5B51%5D=gd&showCol%5B52%5D=gh&showCol%5B53%5D=gp&showCol%5B54%5D=gr&showCol%5B55%5D=tt&showCol%5B56%5D=bs&showCol%5B57%5D=wk&showCol%5B58%5D=sk&showCol%5B59%5D=aw&showCol%5B60%5D=dw&showCol%5B61%5D=ir&showCol%5B62%5D=pac&showCol%5B63%5D=sho&showCol%5B64%5D=pas&showCol%5B65%5D=dri&showCol%5B66%5D=def&showCol%5B67%5D=phy&showCol%5B68%5D=gc&r={}&set=true'.format(dict_of_version['key']),
            'https://sofifa.com/players?showCol%5B0%5D=pi&showCol%5B1%5D=ae&showCol%5B2%5D=hi&showCol%5B3%5D=wi&showCol%5B4%5D=pf&showCol%5B5%5D=oa&showCol%5B6%5D=pt&showCol%5B7%5D=bo&showCol%5B8%5D=bp&showCol%5B9%5D=gu&showCol%5B10%5D=jt&showCol%5B11%5D=le&showCol%5B12%5D=vl&showCol%5B13%5D=wg&showCol%5B14%5D=rc&showCol%5B15%5D=ta&showCol%5B16%5D=cr&showCol%5B17%5D=fi&showCol%5B18%5D=he&showCol%5B19%5D=sh&showCol%5B20%5D=vo&showCol%5B21%5D=ts&showCol%5B22%5D=dr&showCol%5B23%5D=cu&showCol%5B24%5D=fr&ael=29&aeh=31&showCol%5B25%5D=lo&showCol%5B26%5D=bl&showCol%5B27%5D=to&showCol%5B28%5D=ac&showCol%5B29%5D=sp&showCol%5B30%5D=ag&showCol%5B31%5D=re&showCol%5B32%5D=ba&showCol%5B33%5D=tp&showCol%5B34%5D=so&showCol%5B35%5D=ju&showCol%5B36%5D=st&showCol%5B37%5D=sr&showCol%5B38%5D=ln&showCol%5B39%5D=te&showCol%5B40%5D=ar&showCol%5B41%5D=in&showCol%5B42%5D=po&showCol%5B43%5D=vi&showCol%5B44%5D=pe&showCol%5B45%5D=cm&showCol%5B46%5D=td&showCol%5B47%5D=ma&showCol%5B48%5D=sa&showCol%5B49%5D=sl&showCol%5B50%5D=tg&showCol%5B51%5D=gd&showCol%5B52%5D=gh&showCol%5B53%5D=gp&showCol%5B54%5D=gr&showCol%5B55%5D=tt&showCol%5B56%5D=bs&showCol%5B57%5D=wk&showCol%5B58%5D=sk&showCol%5B59%5D=aw&showCol%5B60%5D=dw&showCol%5B61%5D=ir&showCol%5B62%5D=pac&showCol%5B63%5D=sho&showCol%5B64%5D=pas&showCol%5B65%5D=dri&showCol%5B66%5D=def&showCol%5B67%5D=phy&showCol%5B68%5D=gc&r={}&set=true'.format(dict_of_version['key']),
            'https://sofifa.com/players?showCol%5B0%5D=pi&showCol%5B1%5D=ae&showCol%5B2%5D=hi&showCol%5B3%5D=wi&showCol%5B4%5D=pf&showCol%5B5%5D=oa&showCol%5B6%5D=pt&showCol%5B7%5D=bo&showCol%5B8%5D=bp&showCol%5B9%5D=gu&showCol%5B10%5D=jt&showCol%5B11%5D=le&showCol%5B12%5D=vl&showCol%5B13%5D=wg&showCol%5B14%5D=rc&showCol%5B15%5D=ta&showCol%5B16%5D=cr&showCol%5B17%5D=fi&showCol%5B18%5D=he&showCol%5B19%5D=sh&showCol%5B20%5D=vo&showCol%5B21%5D=ts&showCol%5B22%5D=dr&showCol%5B23%5D=cu&showCol%5B24%5D=fr&ael=32&aeh=37&showCol%5B25%5D=lo&showCol%5B26%5D=bl&showCol%5B27%5D=to&showCol%5B28%5D=ac&showCol%5B29%5D=sp&showCol%5B30%5D=ag&showCol%5B31%5D=re&showCol%5B32%5D=ba&showCol%5B33%5D=tp&showCol%5B34%5D=so&showCol%5B35%5D=ju&showCol%5B36%5D=st&showCol%5B37%5D=sr&showCol%5B38%5D=ln&showCol%5B39%5D=te&showCol%5B40%5D=ar&showCol%5B41%5D=in&showCol%5B42%5D=po&showCol%5B43%5D=vi&showCol%5B44%5D=pe&showCol%5B45%5D=cm&showCol%5B46%5D=td&showCol%5B47%5D=ma&showCol%5B48%5D=sa&showCol%5B49%5D=sl&showCol%5B50%5D=tg&showCol%5B51%5D=gd&showCol%5B52%5D=gh&showCol%5B53%5D=gp&showCol%5B54%5D=gr&showCol%5B55%5D=tt&showCol%5B56%5D=bs&showCol%5B57%5D=wk&showCol%5B58%5D=sk&showCol%5B59%5D=aw&showCol%5B60%5D=dw&showCol%5B61%5D=ir&showCol%5B62%5D=pac&showCol%5B63%5D=sho&showCol%5B64%5D=pas&showCol%5B65%5D=dri&showCol%5B66%5D=def&showCol%5B67%5D=phy&showCol%5B68%5D=gc&r={}&set=true'.format(dict_of_version['key']),
            'https://sofifa.com/players?showCol%5B0%5D=pi&showCol%5B1%5D=ae&showCol%5B2%5D=hi&showCol%5B3%5D=wi&showCol%5B4%5D=pf&showCol%5B5%5D=oa&showCol%5B6%5D=pt&showCol%5B7%5D=bo&showCol%5B8%5D=bp&showCol%5B9%5D=gu&showCol%5B10%5D=jt&showCol%5B11%5D=le&showCol%5B12%5D=vl&showCol%5B13%5D=wg&showCol%5B14%5D=rc&showCol%5B15%5D=ta&showCol%5B16%5D=cr&showCol%5B17%5D=fi&showCol%5B18%5D=he&showCol%5B19%5D=sh&showCol%5B20%5D=vo&showCol%5B21%5D=ts&showCol%5B22%5D=dr&showCol%5B23%5D=cu&showCol%5B24%5D=fr&ael=38&showCol%5B25%5D=lo&showCol%5B26%5D=bl&showCol%5B27%5D=to&showCol%5B28%5D=ac&showCol%5B29%5D=sp&showCol%5B30%5D=ag&showCol%5B31%5D=re&showCol%5B32%5D=ba&showCol%5B33%5D=tp&showCol%5B34%5D=so&showCol%5B35%5D=ju&showCol%5B36%5D=st&showCol%5B37%5D=sr&showCol%5B38%5D=ln&showCol%5B39%5D=te&showCol%5B40%5D=ar&showCol%5B41%5D=in&showCol%5B42%5D=po&showCol%5B43%5D=vi&showCol%5B44%5D=pe&showCol%5B45%5D=cm&showCol%5B46%5D=td&showCol%5B47%5D=ma&showCol%5B48%5D=sa&showCol%5B49%5D=sl&showCol%5B50%5D=tg&showCol%5B51%5D=gd&showCol%5B52%5D=gh&showCol%5B53%5D=gp&showCol%5B54%5D=gr&showCol%5B55%5D=tt&showCol%5B56%5D=bs&showCol%5B57%5D=wk&showCol%5B58%5D=sk&showCol%5B59%5D=aw&showCol%5B60%5D=dw&showCol%5B61%5D=ir&showCol%5B62%5D=pac&showCol%5B63%5D=sho&showCol%5B64%5D=pas&showCol%5B65%5D=dri&showCol%5B66%5D=def&showCol%5B67%5D=phy&showCol%5B68%5D=gc&r={}&set=true'.format(dict_of_version['key'])]
                

 

    def parse(self, response):
        #headers = response.css('table.table>thead>tr>th ::text').extract()[5:]
        for player in response.css('table.table>tbody>tr'):
            item = {}
            
            list_={}
            Name = player.css('td.col-name>a::attr(aria-label)').extract()
            print(Name)
            page_ref = player.css('td.col-name>a::attr(href)').get()
            ID=player.css('td.col.col-pi::text').get()
            #ID=player.xpath('/html/body/div[1]/div/div[2]/div/table/tbody/tr[1]/td[7]/text()').extract()
            #print(ID,'dododo')
            # value = list(map(str.strip, [p.css(' ::text').get() for p in player.css('td')[6:]]))
            #item.update(dict(zip(headers, value)))
            #yield item
                #lien_page = Request(url="https://sofifa.com/"+list['page_ref'],callback=self.parse_date,meta={'item': item})
                #yield lien_page
            lien_transfert = Request(url="https://sofifa.com/player/"+str(ID)+"/live",callback=self.parse_transfert,meta={'id':ID,'Name':Name})
            yield lien_transfert
        next_page = response.xpath('//span[@class="bp3-button-text" and text()="Next"]/parent::a/@href').get()

        if next_page:
            yield Request(response.urljoin(next_page))

 

    def parse_date(self, response):
        item = response.meta['item']
        date = response.xpath('//*[@id="body"]/div[2]/div/div[2]/div[1]/div/div/text()').extract()[-1]
        item["birth"] = date.split("(")[1].split(")")[0]
        return item

    def parse_transfert(self, response):
            #headers= response.css()
            ID= response.meta['id']
            Name=response.meta['Name']
            center = response.css('body > div.center > div > div.col.col-12')    #center est la table(objet ) sur laquelle va être appliqué le scrap
            for i in range(1,8):
                transfers =  center.css('div:nth-child({})>h5'.format(i)).extract() #le tableau récupère jusqu'à 7 nom de tableau
                print(transfers)
                if len(transfers)==1:         #condition permettant de savoir s'il existe au moins un tableau dans la fiche "in real life" du joueur
                    if "Transfers" in transfers[0]: #on parcours la boucle si la chaîne de caractère du tableau transfers contient "Transfers"
                        for ltr in center.css('div:nth-child({}) > table > tbody>tr'.format(i)):
                               if "bought" not in ltr.xpath('td[3]/text()').extract()[0] and 'swap' not in ltr.xpath('td[3]/text()').extract()[0]:   #on récupère seulement les lignes sans loan,bought,swap
                                    item ={}
                                    item['ID']=ID
                                    item ['BirthDate']=ltr.xpath('//*[@id="body"]/div[1]/div/div[1]/div[1]/ul[1]/li[2]/text()').extract()
                                    item['Name']=Name     
                                    item["From"]=ltr.css('td:nth-child(1) > a ::text').extract()
                                    if len(item["From"])==0:
                                        item["From"]=ltr.xpath('td[1]/text()').extract()
                                    item["To"]=ltr.css('td:nth-child(2) > a::text').extract()
                                    if len(item["To"])==0:
                                        item["To"]=ltr.xpath('td[2]/text()').extract()
                                    item["ID_From"]=ltr.css('td:nth-child(1) > a::attr(href)').extract()#[0].split("/")[2]
                                    item["ID_To"]=ltr.css('td:nth-child(2) > a::attr(href)').extract()#[0].split("/")[2]
                                    item["Date"]=ltr.xpath('td[4]/text()').extract()
                                    item["Prix"]=ltr.xpath('td[3]/text()').extract()
                                    #item["Saison"]=comp_date(item["Date"][0])zDX
                                    #item["Prix_Converti"]=convert_prix(ltr.xpath('td[3]/text()').extract()[0])
                                    if "loan" in item["Prix"]:
                                        item["Nature"]="loan"
                                    else:
                                        item["Nature"]="transfert"
                                    yield item
                            