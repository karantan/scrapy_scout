# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyScoutItem(scrapy.Item):
    date = scrapy.Field()
    priglasitelj = scrapy.Field()
    privzeto_podjetje = scrapy.Field()
    sektor = scrapy.Field()
    st_zadeve = scrapy.Field()
