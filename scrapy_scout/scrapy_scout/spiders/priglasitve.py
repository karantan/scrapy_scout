# -*- coding: utf-8 -*-
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
        i = ScrapyScoutItem()
        doc = pq(response.body)
        import pdb
        pdb.set_trace()
