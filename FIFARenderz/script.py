import scrapy
import numpy as np
import pandas as pd
from csv import writer

class FifaSpider(scrapy.Spider):
    name = "fifa"

    def start_requests(self):
        overview_headers = np.array(['Skillboost', 'Club', 'Nation', 'Foot', 'Weak Foot', 'Height', 'Weight', 'Workrates (ATT/DEF)', 'Source'])
        pd.DataFrame(columns=overview_headers).to_csv("data/overview.csv", index = False)
        pattern = 'https://fifarenderz.com/20/players?page='
        urls = []
        for i in range(1,20):
            urls.append(pattern+str(i))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parsePlayerList)
    
    def parsePlayerList(self,response):
        page = response.url

        if(page.split('/')[-2]!='player'):
            page = response.url.split("?")[1]
            page = page[5:]
            fpath = 'data/List_pages/'
            filename = 'Page_%s.html' % page
            with open(fpath+filename, 'wb') as f:
                f.write(response.body)
            self.log('Saved file %s' % filename)
            next_urls = response.css('div.player-filtering-body a::attr(href)').getall()
            for url in next_urls:
                if url is not None:
                    next_page = response.urljoin(url)
                    yield scrapy.Request(next_page, callback=self.parsePlayer)
        else:
            self.log('Wierd site %s',response.url)

    def parsePlayer(self, response):
        page = response.url

        if(page.split('/')[-2]=='player'):
            page = response.url.split("/")[-1]
            fpath = 'data/Player_pages/'
            filename = 'Player_%s.html' % page
            with open(fpath+filename, 'wb') as f:
                f.write(response.body)
            self.log('Saved file %s' % filename)
            overview = response.css('tbody.player-info-table')
            data = [''.join(sel.css('::text').getall()).strip() for sel in overview.css('tr td')]
            row = []
            for i in range(1,len(data),2):
                row.append(data[i])
            print(row)

            with open("data/overview.csv", "a+") as ofile:
                csv_writer = writer(ofile)
                csv_writer.writerow(row)

        else:
            self.log('Wierd site %s',response.url)

        
    