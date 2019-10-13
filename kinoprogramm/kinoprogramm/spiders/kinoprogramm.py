import locale
from datetime import datetime
from typing import List

import scrapy

from .data_structures import Cinema, Address, Contact, Show


class KinoSpider(scrapy.Spider):
    name = 'kinoprogramm'
    start_urls = ['https://www.berlin.de/kino/_bin/azfilm.php']

    @staticmethod
    def is_positiveinteger(s: str) -> bool:
        try:
            if int(s) > 0:
                return True
        except ValueError:
            return False
        return False

    @staticmethod
    def create_shows(titles: List[str], movies_times: List[List[str]]) -> List[Show]:

        # in order to be able to parse weekdays
        locale.setlocale(locale.LC_TIME, 'de_DE')

        shows = list()

        for title, movie_times in zip(titles, movies_times):
            show = Show(title=title)
            for show_day, show_times in zip(*[iter(movie_times)] * 2):
                for show_time in show_times.split(','):

                    show.times.append(datetime.strptime(show_day + show_time,
                                                        '%a, %d.%m.%y: %H:%M'))

            shows.append(show)
        return shows

    def parse(self, response):

        selectors = response.xpath('//div[@class="controls"]/select/option')

        hrefs = ['https://www.berlin.de/kino/_bin/kinodetail.php/' + sel.attrib['value']
                 for sel in selectors if self.is_positiveinteger(sel.attrib['value'])]

        for href in hrefs:
            yield response.follow(href, self.parse_cinema)

    def parse_cinema(self, response):

        titles = response.css('button.accordion-trigger::text').getall()
        movies_times = [div.xpath('//table//td/text()').getall()
                        for div in response.css('div.table-responsive-wrapper')]

        cinema = Cinema()
        cinema.name = response.css('h1.top::text').get()
        cinema.description = response.xpath('//div[@class="kinodetail echo"]/p/text()').get()
        """
        cinema.address = Address(street=response.xpath('//span[@class="street-address"]/text()').get(),
                                 postal_code=response.xpath('//span[@class="postal-code"]/text()').get(),
                                 district=response.xpath('//span[@class="locality"]/text()').get(),
                                 city='Berlin',
                                 country='Germany')
        
        cinema.contact = Contact(telephone=response.xpath(
            '//span[contains(text(), "Telefon")]/following-sibling::span/text()').get())
        """

        cinema.prices = response.xpath('//section[@class="infoblock oeffnungszeiten"]/div/*/text()').getall()

        """
        cinema.shows = self.create_shows(titles, movies_times)
        """

        yield cinema.__dict__
