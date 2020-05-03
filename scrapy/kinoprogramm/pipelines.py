# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import logging
from datetime import datetime
from gzip import GzipFile
from io import BytesIO

import boto3
import pymongo
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings


class KinoprogrammPipeline(object):

    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):
    """
    Pipeline to write items to MongoDB
    """

    def __init__(self):

        logger = logging.getLogger('MongoDBPipeline')
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
        self.logger.info(f'item {item["name"]} from spider {spider.name} added to MongoDB')

        return item


class S3Pipeline(object):
    """
    Pipeline to write items to AWS S3
    """

    def __init__(self):
        logger = logging.getLogger('S3Pipeline')
        self.logger = logger

        self.bucket = 'kinoprogramm-scraper'
        self.base_path = 'berlin-de'

        session = boto3.session.Session()
        self.s3_client = session.client(service_name='s3')
        self.s3_resource = session.resource('s3')

    def process_item(self, item, spider):

        # partitions year / month / day
        today = datetime.today()
        year = str(today.year)
        month = str(today.month).zfill(2)
        day = str(today.day).zfill(2)
        path = f'berlin-de/year={year}/month={month}/day={day}'
        filename = f'scrapy_{item["name"].replace(" ", "-").replace("/", "-")}.json.gz'
        full_path = f'{self.bucket}/{path}/{filename}'

        def date_converter(d):
            if isinstance(d, datetime):
                return d.isoformat()

        body = json.dumps(item, default=date_converter, ensure_ascii=False)

        # write gzip-compressed json files
        gz_body = BytesIO()
        with GzipFile(None, 'wb', 9, gz_body) as gz:
            # convert unicode strings to bytes
            _ = gz.write(body.encode('utf-8'))

        try:
            self.s3_client.put_object(
                Body=gz_body.getvalue(),
                ContentEncoding='gzip',
                Bucket=self.bucket, Key=f'{path}/{filename}')

        except Exception as e:
            msg = f'Exception writing parsed jobs to S3: /{full_path}'
            self.logger.error(msg)
            self.logger.error(e)
        else:
            self.logger.info(f'Item {item["name"]} from spider {spider.name} added to S3: {full_path}')
        return item
