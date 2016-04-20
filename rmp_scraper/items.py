# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProfessorItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    fname = scrapy.Field()
    fname2 = scrapy.Field()
    lname = scrapy.Field()
    campus = scrapy.Field()
    quality = scrapy.Field()
    avg = scrapy.Field()
    help = scrapy.Field()
    easiness = scrapy.Field()
    chili = scrapy.Field()
    clarity = scrapy.Field()
    comment_text = scrapy.Field()
    comment_type = scrapy.Field()
    comment_course = scrapy.Field()
    tag = scrapy.Field()
