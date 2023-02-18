# -*- coding: utf-8 -*-
#from this import d
import scrapy
from scrapy import Request
import re
import joblib
from extract_historique import dict_of_version
dict_of_version=joblib.load("fifa20\\spiders\\date.pkl")

def rename_header(list_headers,patt,rep):
    """_summary_

    Args:
        list_headers (_type_): _description_
        patt (_type_): _description_
        rep (_type_): _description_

    Returns:
        _type_: _description_
    """
    if isinstance(patt, list):
        for p in patt:
            try :
                element_index = list_headers.index(p)
                if isinstance(element_index,int):
                    list_headers[element_index] = rep
            except Exception as e:
                print(e)
        return list_headers
    else: 
        try :
            element_index = list_headers.index(patt)
            if isinstance(element_index,int):
                list_headers[element_index] = rep
        except Exception as e:
            print(e)
        return list_headers
class SofifaSpider(scrapy.Spider):
    name = 'stats_quali'
    allowed_domains = ['sofifa.com']
    start_urls = ['https://sofifa.com/players?showCol%5B0%5D=pi&showCol%5B1%5D=ae&showCol%5B2%5D=hi&showCol%5B3%5D=wi&showCol%5B4%5D=pf&showCol%5B5%5D=oa&showCol%5B6%5D=pt&showCol%5B7%5D=bo&showCol%5B8%5D=bp&showCol%5B9%5D=gu&showCol%5B10%5D=jt&showCol%5B11%5D=le&showCol%5B12%5D=vl&showCol%5B13%5D=wg&showCol%5B14%5D=rc&showCol%5B15%5D=ta&showCol%5B16%5D=cr&showCol%5B17%5D=fi&showCol%5B18%5D=he&showCol%5B19%5D=sh&showCol%5B20%5D=vo&showCol%5B21%5D=ts&showCol%5B22%5D=dr&showCol%5B23%5D=cu&showCol%5B24%5D=fr&aeh=20&showCol%5B25%5D=lo&showCol%5B26%5D=bl&showCol%5B27%5D=to&showCol%5B28%5D=ac&showCol%5B29%5D=sp&showCol%5B30%5D=ag&showCol%5B31%5D=re&showCol%5B32%5D=ba&showCol%5B33%5D=tp&showCol%5B34%5D=so&showCol%5B35%5D=ju&showCol%5B36%5D=st&showCol%5B37%5D=sr&showCol%5B38%5D=ln&showCol%5B39%5D=te&showCol%5B40%5D=ar&showCol%5B41%5D=in&showCol%5B42%5D=po&showCol%5B43%5D=vi&showCol%5B44%5D=pe&showCol%5B45%5D=cm&showCol%5B46%5D=td&showCol%5B47%5D=ma&showCol%5B48%5D=sa&showCol%5B49%5D=sl&showCol%5B50%5D=tg&showCol%5B51%5D=gd&showCol%5B52%5D=gh&showCol%5B53%5D=gp&showCol%5B54%5D=gr&showCol%5B55%5D=tt&showCol%5B56%5D=bs&showCol%5B57%5D=wk&showCol%5B58%5D=sk&showCol%5B59%5D=aw&showCol%5B60%5D=dw&showCol%5B61%5D=ir&showCol%5B62%5D=pac&showCol%5B63%5D=sho&showCol%5B64%5D=pas&showCol%5B65%5D=dri&showCol%5B66%5D=def&showCol%5B67%5D=phy&showCol%5B68%5D=gc&r={}&set=true'.format(dict_of_version['key']),
                'https://sofifa.com/players?showCol%5B0%5D=pi&showCol%5B1%5D=ae&showCol%5B2%5D=hi&showCol%5B3%5D=wi&showCol%5B4%5D=pf&showCol%5B5%5D=oa&showCol%5B6%5D=pt&showCol%5B7%5D=bo&showCol%5B8%5D=bp&showCol%5B9%5D=gu&showCol%5B10%5D=jt&showCol%5B11%5D=le&showCol%5B12%5D=vl&showCol%5B13%5D=wg&showCol%5B14%5D=rc&showCol%5B15%5D=ta&showCol%5B16%5D=cr&showCol%5B17%5D=fi&showCol%5B18%5D=he&showCol%5B19%5D=sh&showCol%5B20%5D=vo&showCol%5B21%5D=ts&showCol%5B22%5D=dr&showCol%5B23%5D=cu&showCol%5B24%5D=fr&ael=21&aeh=24&showCol%5B25%5D=lo&showCol%5B26%5D=bl&showCol%5B27%5D=to&showCol%5B28%5D=ac&showCol%5B29%5D=sp&showCol%5B30%5D=ag&showCol%5B31%5D=re&showCol%5B32%5D=ba&showCol%5B33%5D=tp&showCol%5B34%5D=so&showCol%5B35%5D=ju&showCol%5B36%5D=st&showCol%5B37%5D=sr&showCol%5B38%5D=ln&showCol%5B39%5D=te&showCol%5B40%5D=ar&showCol%5B41%5D=in&showCol%5B42%5D=po&showCol%5B43%5D=vi&showCol%5B44%5D=pe&showCol%5B45%5D=cm&showCol%5B46%5D=td&showCol%5B47%5D=ma&showCol%5B48%5D=sa&showCol%5B49%5D=sl&showCol%5B50%5D=tg&showCol%5B51%5D=gd&showCol%5B52%5D=gh&showCol%5B53%5D=gp&showCol%5B54%5D=gr&showCol%5B55%5D=tt&showCol%5B56%5D=bs&showCol%5B57%5D=wk&showCol%5B58%5D=sk&showCol%5B59%5D=aw&showCol%5B60%5D=dw&showCol%5B61%5D=ir&showCol%5B62%5D=pac&showCol%5B63%5D=sho&showCol%5B64%5D=pas&showCol%5B65%5D=dri&showCol%5B66%5D=def&showCol%5B67%5D=phy&showCol%5B68%5D=gc&r={}&set=true'.format(dict_of_version['key']),
                'https://sofifa.com/players?showCol%5B0%5D=pi&showCol%5B1%5D=ae&showCol%5B2%5D=hi&showCol%5B3%5D=wi&showCol%5B4%5D=pf&showCol%5B5%5D=oa&showCol%5B6%5D=pt&showCol%5B7%5D=bo&showCol%5B8%5D=bp&showCol%5B9%5D=gu&showCol%5B10%5D=jt&showCol%5B11%5D=le&showCol%5B12%5D=vl&showCol%5B13%5D=wg&showCol%5B14%5D=rc&showCol%5B15%5D=ta&showCol%5B16%5D=cr&showCol%5B17%5D=fi&showCol%5B18%5D=he&showCol%5B19%5D=sh&showCol%5B20%5D=vo&showCol%5B21%5D=ts&showCol%5B22%5D=dr&showCol%5B23%5D=cu&showCol%5B24%5D=fr&ael=25&aeh=29&showCol%5B25%5D=lo&showCol%5B26%5D=bl&showCol%5B27%5D=to&showCol%5B28%5D=ac&showCol%5B29%5D=sp&showCol%5B30%5D=ag&showCol%5B31%5D=re&showCol%5B32%5D=ba&showCol%5B33%5D=tp&showCol%5B34%5D=so&showCol%5B35%5D=ju&showCol%5B36%5D=st&showCol%5B37%5D=sr&showCol%5B38%5D=ln&showCol%5B39%5D=te&showCol%5B40%5D=ar&showCol%5B41%5D=in&showCol%5B42%5D=po&showCol%5B43%5D=vi&showCol%5B44%5D=pe&showCol%5B45%5D=cm&showCol%5B46%5D=td&showCol%5B47%5D=ma&showCol%5B48%5D=sa&showCol%5B49%5D=sl&showCol%5B50%5D=tg&showCol%5B51%5D=gd&showCol%5B52%5D=gh&showCol%5B53%5D=gp&showCol%5B54%5D=gr&showCol%5B55%5D=tt&showCol%5B56%5D=bs&showCol%5B57%5D=wk&showCol%5B58%5D=sk&showCol%5B59%5D=aw&showCol%5B60%5D=dw&showCol%5B61%5D=ir&showCol%5B62%5D=pac&showCol%5B63%5D=sho&showCol%5B64%5D=pas&showCol%5B65%5D=dri&showCol%5B66%5D=def&showCol%5B67%5D=phy&showCol%5B68%5D=gc&r={}&set=true'.format(dict_of_version['key']),
                'https://sofifa.com/players?showCol%5B0%5D=pi&showCol%5B1%5D=ae&showCol%5B2%5D=hi&showCol%5B3%5D=wi&showCol%5B4%5D=pf&showCol%5B5%5D=oa&showCol%5B6%5D=pt&showCol%5B7%5D=bo&showCol%5B8%5D=bp&showCol%5B9%5D=gu&showCol%5B10%5D=jt&showCol%5B11%5D=le&showCol%5B12%5D=vl&showCol%5B13%5D=wg&showCol%5B14%5D=rc&showCol%5B15%5D=ta&showCol%5B16%5D=cr&showCol%5B17%5D=fi&showCol%5B18%5D=he&showCol%5B19%5D=sh&showCol%5B20%5D=vo&showCol%5B21%5D=ts&showCol%5B22%5D=dr&showCol%5B23%5D=cu&showCol%5B24%5D=fr&ael=30&aeh=34&showCol%5B25%5D=lo&showCol%5B26%5D=bl&showCol%5B27%5D=to&showCol%5B28%5D=ac&showCol%5B29%5D=sp&showCol%5B30%5D=ag&showCol%5B31%5D=re&showCol%5B32%5D=ba&showCol%5B33%5D=tp&showCol%5B34%5D=so&showCol%5B35%5D=ju&showCol%5B36%5D=st&showCol%5B37%5D=sr&showCol%5B38%5D=ln&showCol%5B39%5D=te&showCol%5B40%5D=ar&showCol%5B41%5D=in&showCol%5B42%5D=po&showCol%5B43%5D=vi&showCol%5B44%5D=pe&showCol%5B45%5D=cm&showCol%5B46%5D=td&showCol%5B47%5D=ma&showCol%5B48%5D=sa&showCol%5B49%5D=sl&showCol%5B50%5D=tg&showCol%5B51%5D=gd&showCol%5B52%5D=gh&showCol%5B53%5D=gp&showCol%5B54%5D=gr&showCol%5B55%5D=tt&showCol%5B56%5D=bs&showCol%5B57%5D=wk&showCol%5B58%5D=sk&showCol%5B59%5D=aw&showCol%5B60%5D=dw&showCol%5B61%5D=ir&showCol%5B62%5D=pac&showCol%5B63%5D=sho&showCol%5B64%5D=pas&showCol%5B65%5D=dri&showCol%5B66%5D=def&showCol%5B67%5D=phy&showCol%5B68%5D=gc&r={}&set=true'.format(dict_of_version['key']),
                'https://sofifa.com/players?showCol%5B0%5D=pi&showCol%5B1%5D=ae&showCol%5B2%5D=hi&showCol%5B3%5D=wi&showCol%5B4%5D=pf&showCol%5B5%5D=oa&showCol%5B6%5D=pt&showCol%5B7%5D=bo&showCol%5B8%5D=bp&showCol%5B9%5D=gu&showCol%5B10%5D=jt&showCol%5B11%5D=le&showCol%5B12%5D=vl&showCol%5B13%5D=wg&showCol%5B14%5D=rc&showCol%5B15%5D=ta&showCol%5B16%5D=cr&showCol%5B17%5D=fi&showCol%5B18%5D=he&showCol%5B19%5D=sh&showCol%5B20%5D=vo&showCol%5B21%5D=ts&showCol%5B22%5D=dr&showCol%5B23%5D=cu&showCol%5B24%5D=fr&ael=35&aeh=37&showCol%5B25%5D=lo&showCol%5B26%5D=bl&showCol%5B27%5D=to&showCol%5B28%5D=ac&showCol%5B29%5D=sp&showCol%5B30%5D=ag&showCol%5B31%5D=re&showCol%5B32%5D=ba&showCol%5B33%5D=tp&showCol%5B34%5D=so&showCol%5B35%5D=ju&showCol%5B36%5D=st&showCol%5B37%5D=sr&showCol%5B38%5D=ln&showCol%5B39%5D=te&showCol%5B40%5D=ar&showCol%5B41%5D=in&showCol%5B42%5D=po&showCol%5B43%5D=vi&showCol%5B44%5D=pe&showCol%5B45%5D=cm&showCol%5B46%5D=td&showCol%5B47%5D=ma&showCol%5B48%5D=sa&showCol%5B49%5D=sl&showCol%5B50%5D=tg&showCol%5B51%5D=gd&showCol%5B52%5D=gh&showCol%5B53%5D=gp&showCol%5B54%5D=gr&showCol%5B55%5D=tt&showCol%5B56%5D=bs&showCol%5B57%5D=wk&showCol%5B58%5D=sk&showCol%5B59%5D=aw&showCol%5B60%5D=dw&showCol%5B61%5D=ir&showCol%5B62%5D=pac&showCol%5B63%5D=sho&showCol%5B64%5D=pas&showCol%5B65%5D=dri&showCol%5B66%5D=def&showCol%5B67%5D=phy&showCol%5B68%5D=gc&r={}&set=true'.format(dict_of_version['key']),
                'https://sofifa.com/players?showCol%5B0%5D=pi&showCol%5B1%5D=ae&showCol%5B2%5D=hi&showCol%5B3%5D=wi&showCol%5B4%5D=pf&showCol%5B5%5D=oa&showCol%5B6%5D=pt&showCol%5B7%5D=bo&showCol%5B8%5D=bp&showCol%5B9%5D=gu&showCol%5B10%5D=jt&showCol%5B11%5D=le&showCol%5B12%5D=vl&showCol%5B13%5D=wg&showCol%5B14%5D=rc&showCol%5B15%5D=ta&showCol%5B16%5D=cr&showCol%5B17%5D=fi&showCol%5B18%5D=he&showCol%5B19%5D=sh&showCol%5B20%5D=vo&showCol%5B21%5D=ts&showCol%5B22%5D=dr&showCol%5B23%5D=cu&showCol%5B24%5D=fr&ael=38&aeh=39&showCol%5B25%5D=lo&showCol%5B26%5D=bl&showCol%5B27%5D=to&showCol%5B28%5D=ac&showCol%5B29%5D=sp&showCol%5B30%5D=ag&showCol%5B31%5D=re&showCol%5B32%5D=ba&showCol%5B33%5D=tp&showCol%5B34%5D=so&showCol%5B35%5D=ju&showCol%5B36%5D=st&showCol%5B37%5D=sr&showCol%5B38%5D=ln&showCol%5B39%5D=te&showCol%5B40%5D=ar&showCol%5B41%5D=in&showCol%5B42%5D=po&showCol%5B43%5D=vi&showCol%5B44%5D=pe&showCol%5B45%5D=cm&showCol%5B46%5D=td&showCol%5B47%5D=ma&showCol%5B48%5D=sa&showCol%5B49%5D=sl&showCol%5B50%5D=tg&showCol%5B51%5D=gd&showCol%5B52%5D=gh&showCol%5B53%5D=gp&showCol%5B54%5D=gr&showCol%5B55%5D=tt&showCol%5B56%5D=bs&showCol%5B57%5D=wk&showCol%5B58%5D=sk&showCol%5B59%5D=aw&showCol%5B60%5D=dw&showCol%5B61%5D=ir&showCol%5B62%5D=pac&showCol%5B63%5D=sho&showCol%5B64%5D=pas&showCol%5B65%5D=dri&showCol%5B66%5D=def&showCol%5B67%5D=phy&showCol%5B68%5D=gc&r={}&set=true'.format(dict_of_version['key']),
                'https://sofifa.com/players?showCol%5B0%5D=pi&showCol%5B1%5D=ae&showCol%5B2%5D=hi&showCol%5B3%5D=wi&showCol%5B4%5D=pf&showCol%5B5%5D=oa&showCol%5B6%5D=pt&showCol%5B7%5D=bo&showCol%5B8%5D=bp&showCol%5B9%5D=gu&showCol%5B10%5D=jt&showCol%5B11%5D=le&showCol%5B12%5D=vl&showCol%5B13%5D=wg&showCol%5B14%5D=rc&showCol%5B15%5D=ta&showCol%5B16%5D=cr&showCol%5B17%5D=fi&showCol%5B18%5D=he&showCol%5B19%5D=sh&showCol%5B20%5D=vo&showCol%5B21%5D=ts&showCol%5B22%5D=dr&showCol%5B23%5D=cu&showCol%5B24%5D=fr&ael=40&showCol%5B25%5D=lo&showCol%5B26%5D=bl&showCol%5B27%5D=to&showCol%5B28%5D=ac&showCol%5B29%5D=sp&showCol%5B30%5D=ag&showCol%5B31%5D=re&showCol%5B32%5D=ba&showCol%5B33%5D=tp&showCol%5B34%5D=so&showCol%5B35%5D=ju&showCol%5B36%5D=st&showCol%5B37%5D=sr&showCol%5B38%5D=ln&showCol%5B39%5D=te&showCol%5B40%5D=ar&showCol%5B41%5D=in&showCol%5B42%5D=po&showCol%5B43%5D=vi&showCol%5B44%5D=pe&showCol%5B45%5D=cm&showCol%5B46%5D=td&showCol%5B47%5D=ma&showCol%5B48%5D=sa&showCol%5B49%5D=sl&showCol%5B50%5D=tg&showCol%5B51%5D=gd&showCol%5B52%5D=gh&showCol%5B53%5D=gp&showCol%5B54%5D=gr&showCol%5B55%5D=tt&showCol%5B56%5D=bs&showCol%5B57%5D=wk&showCol%5B58%5D=sk&showCol%5B59%5D=aw&showCol%5B60%5D=dw&showCol%5B61%5D=ir&showCol%5B62%5D=pac&showCol%5B63%5D=sho&showCol%5B64%5D=pas&showCol%5B65%5D=dri&showCol%5B66%5D=def&showCol%5B67%5D=phy&showCol%5B68%5D=gc&r={}&set=true'.format(dict_of_version['key'])]
    def parse(self, response):
        headers = response.css('table.table>thead>tr>th ::text').extract()[5:]
        headers = [header.replace(' ',"") for header in headers]
        # headers = rename_header(list_headers=headers,patt="BOV",rep="best_overal" )
        # headers = rename_header(list_headers=headers,patt="foot",rep="PreferredFoot" )
        # headers = rename_header(list_headers=headers,patt='W/F',rep="WeakFoot" )
        # headers = rename_header(list_headers=headers,patt='SM',rep="SkillMoves" )
        # headers = rename_header(list_headers=headers,patt='StandingTackle',rep="StandTackle" )
        # headers = rename_header(list_headers=headers,patt='SlidingTackle',rep="SlideTackle" )
        # headers = rename_header(list_headers=headers,patt='Positioning',rep="AttPosition" )
        # headers = rename_header(list_headers=headers,patt='ShortPassing',rep="ShortPass" )
        # headers = rename_header(list_headers=headers,patt='HeadingAccuracy',rep="Heading" )
        # headers = rename_header(list_headers=headers,patt='FKAccuracy',rep="FKAcc" )
        # headers = rename_header(list_headers=headers,patt='LongPassing',rep="LongPass" )

        headers = rename_header(list_headers=headers,patt=["BestOverall","BOV"],rep="best_overal" )
        headers = rename_header(list_headers=headers,patt="foot",rep="PreferredFoot" )
        headers = rename_header(list_headers=headers,patt=['WeakFoot','W/F'],rep="WeakFoot" )
        headers = rename_header(list_headers=headers,patt=['SkillMoves','SM'],rep="SkillMoves" )
        headers = rename_header(list_headers=headers,patt='StandingTackle',rep="StandTackle" )
        headers = rename_header(list_headers=headers,patt='SlidingTackle',rep="SlideTackle" )
        headers = rename_header(list_headers=headers,patt='Positioning',rep="AttPosition" )
        headers = rename_header(list_headers=headers,patt='ShortPassing',rep="ShortPass" )
        headers = rename_header(list_headers=headers,patt='HeadingAccuracy',rep="Heading" )
        headers = rename_header(list_headers=headers,patt='FKAccuracy',rep="FKAcc" )
        headers = rename_header(list_headers=headers,patt='LongPassing',rep="LongPass" )

        for player in response.css('table.table>tbody>tr'):
            item = {}
            
            item['Name'] = player.css('td.col-name>a::attr(aria-label)').extract()
            item['page_ref'] = player.css('td.col-name>a::attr(href)').get()
            item['Image'] = player.css('figure.avatar>img::attr(data-src)').get()
            item['Natinality'] = player.css('td.col-name>img::attr(title)').get()
            item['PreferredPositions'] = '/'.join(player.css('td.col-name span.pos ::text').extract())
            item['Age'] = player.css('td.col-ae ::text').get()
            item['Overal'] = player.css('td.col-oa ::text').get()
            item['Potential'] = player.css('td.col-pt ::text').get()
            item['Club'] = player.css('td.col-name')[1].css('a ::text').get()

            value = list(map(str.strip, [str(p.css(' ::text').get()) for p in player.css('td')[6:]]))
            item.update(dict(zip(headers, value)))
            #yield item
            try:
                item["PlayerWorkRate"] = item['A/W']+"/"+item["D/W"]
            except:
                item["PlayerWorkRate"] = item['AttackingWorkRate']+"/"+item["DefensiveWorkRate"] 
            
            lien_page = Request(url="https://sofifa.com"+item['page_ref'],callback=self.parse_date,meta={'item': item})

            yield lien_page

        next_page = response.xpath('//span[@class="bp3-button-text" and text()="Next"]/parent::a/@href').get()

        if next_page:
            yield Request(response.urljoin(next_page))
    def parse_date(self, response):
        item = response.meta['item']

        date = response.xpath('//*[@id="body"]/div[2]/div/div[2]/div[1]/div/div/text()').extract()[-1]
        item["BirthDate"] = date.split("(")[1].split(")")[0]
        spec = response.xpath('//*[@id="body"]/div[2]/div/div[2]/div[3]/div/ul').get()
        list_spec = re.findall("\#[\w\s]+",spec.replace("\xa0",""))
        item["Specialities"] = '/'.join(list_spec).replace("#","")
        item["Club_ContractLength"] = response.xpath('//*[@id="body"]/div[2]/div/div[2]/div[4]/div/ul/li[5]/text()').extract()
        item["Club_Position"] = response.css('#body > div:nth-child(5) > div > div.col.col-12 > div:nth-child(4) > div > ul > li:nth-child(2) > span ::text').get()
        return item 