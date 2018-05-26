# -*- coding: utf-8 -*-
from datetime import datetime
from pyquery import PyQuery as pq
from scrapy_scout.items import ScrapyScoutItem

import scrapy


class PriglasitveSpider(scrapy.Spider):
    name = 'priglasitve'
    allowed_domains = ['varstvo-konkurence.si']
    start_urls = [
        'http://www.varstvo-konkurence.si/koncentracije-podjetij/'
        'priglasene-koncentracije-in-odlocitve/',
    ]

    def parse(self, response):
        doc = pq(response.body)
        table_rows = doc(".contenttable tbody tr")

        for row in table_rows:
            yield ScrapyScoutItem(
                date=datetime.strptime(
                    row[0].text_content().strip(), '%d.%m.%Y'),
                priglasitelj=row[1].text_content().strip(),
                privzeto_podjetje=row[2].text_content().strip(),
                sektor=row[3].text_content().strip(),
                st_zadeve=row[4].text_content().strip(),
            )
