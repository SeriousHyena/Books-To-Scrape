# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Scrape3Item(scrapy.Item):
    book_title = scrapy.Field()
    book_availability = scrapy.Field()
    book_price = scrapy.Field()
    review_text = scrapy.Field()
