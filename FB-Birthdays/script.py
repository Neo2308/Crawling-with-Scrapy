import scrapy
from scrapy import FormRequest
import numpy as np
import pandas as pd
import json
import os
from csv import writer
import datetime
import calendar
class FbBDaySpider(scrapy.Spider):
    name = "Birthdays"

    def start_requests(self):
        cwd = os.path.dirname(os.path.abspath(__file__))
        webPath = os.path.join(cwd,os.path.join('data','Birthdays.html'))
        url = 'file://'+webPath
        yield scrapy.Request(url=url, callback=self.parseBDayList)
    
    def parseBDayList(self,response):
        page = response.url
        if page.split('/')[-1] == 'Birthdays.html':
            filename = 'BDays.json'
            filepath = os.path.join('data',filename)
            data = {}
            boxes = response.css("li._55ws._5as-")
            nameday = boxes.css("p::text").getall()
            for i in range(len(nameday)//2):
                name = nameday[i*2]
                day1 = nameday[i*2+1]
                day2 = datetime.datetime.strptime(day1,'%A, %B %d, %Y')
                day = '{:0>2}'.format(day2.day)
                month = '{:0>2} {}'.format(day2.month,calendar.month_name[day2.month])
                if month not in data:
                    data[month] = {}
                if day not in data[month]:
                    data[month][day] = []
                if name not in data[month][day]:
                    data[month][day].append(name)
            with open(filepath, 'w') as json_file:
                json.dump(data, json_file,indent = 4,sort_keys=True)
            self.log('Saved file %s' % filename)
            
        else:
            self.log('Wierd site %s',response.url)