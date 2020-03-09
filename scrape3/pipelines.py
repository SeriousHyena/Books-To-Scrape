# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo #Python driver for the mongo database



class MongoPipeline(object):
    collection_name = 'books'

#
    def __init__(self):
        self.conn = pymongo.MongoClient(
            'localhost', #the location of the database
            27017 # The port number of the database
        )
        db = self.conn['Book_Store'] # Create a database
        self.collection = db['books_table'] #Create a table to store the data

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item