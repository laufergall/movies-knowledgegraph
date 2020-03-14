"""
use the API to run Scrapy from this script, instead of the typical way of running Scrapy via scrapy crawl.
"""

from kinoprogramm.spiders.kinoprogramm import KinoSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
process.crawl(KinoSpider)
process.start()
