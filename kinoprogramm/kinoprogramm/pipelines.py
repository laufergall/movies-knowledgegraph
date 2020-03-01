# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import os
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import DropItem
import logging


class KinoprogrammPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):

    def __init__(self):

        logger = logging.getLogger('MongoDBPipeline')
        logger.setLevel(logging.DEBUG)
        ch = logging.FileHandler(os.path.join('..', 'data', 'logs', 'MongoDBPipeline.log'))
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        self.logger = logger

        settings = get_project_settings()

        client = pymongo.MongoClient(
            host=settings['MONGODB_HOST'],
            port=settings['MONGODB_PORT'],
            username=settings['MONGODB_USERNAME'],
            password=settings['MONGODB_PASSWORD'],
        )
        db = client[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):

        for data in item:
            if not data:
                raise DropItem(f'Missing {data}!')

        self.collection.insert(dict(item))
        self.logger.debug(f'item {item["name"]} from spyder {spider.name} added to MongoDB')

        return item
