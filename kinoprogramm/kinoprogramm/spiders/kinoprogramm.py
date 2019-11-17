import locale
from datetime import datetime
from typing import List
from .utils import strip_text, is_positiveinteger

import scrapy

from .data_structures import Cinema, Address, Contact, Show


class KinoSpider(scrapy.Spider):
    
    name = 'kinoprogramm'
    start_urls = ['https://www.berlin.de/kino/_bin/azfilm.php']

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

    def parse(self, response: scrapy.http.response.html.HtmlResponse):

        selectors = response.xpath('//div[@class="controls"]/select/option')

        hrefs = ['https://www.berlin.de/kino/_bin/kinodetail.php/' + sel.attrib['value']
                 for sel in selectors if is_positiveinteger(sel.attrib['value'])]

        for href in hrefs:
            yield response.follow(href, self.parse_cinema)

    @strip_text
    def get_titles(self, response: scrapy.http.response.html.HtmlResponse) -> List[str]:
        return response.css('button.accordion-trigger::text').getall()

    @strip_text
    def get_name(self, response: scrapy.http.response.html.HtmlResponse) -> str:
        return response.css('h1.top::text').get()

    @strip_text
    def get_description(self, response: scrapy.http.response.html.HtmlResponse) -> str:
        return response.xpath('//div[@class="kinodetail echo"]/p/text()').get()

    @strip_text
    def get_description(self, response: scrapy.http.response.html.HtmlResponse) -> str:
        return response.xpath('//div[@class="kinodetail echo"]/p/text()').get()

    @strip_text
    def get_description(self, response: scrapy.http.response.html.HtmlResponse) -> str:
        return response.xpath('//div[@class="kinodetail echo"]/p/text()').get()

    @strip_text
    def get_street(self, response: scrapy.http.response.html.HtmlResponse) -> str:
        return response.xpath('//span[@class="street-address"]/text()').get()

    @strip_text
    def get_postal_code(self, response: scrapy.http.response.html.HtmlResponse) -> str:
        return response.xpath('//span[@class="postal-code"]/text()').get()

    @strip_text
    def get_district(self, response: scrapy.http.response.html.HtmlResponse) -> str:
        return response.xpath('//span[@class="locality"]/text()').get()

    @strip_text
    def get_telephone(self, response: scrapy.http.response.html.HtmlResponse) -> str:
        return response.xpath(
                '//span[contains(text(), "Telefon")]/following-sibling::span/text()').get()

    @strip_text
    def get_prices(self, response: scrapy.http.response.html.HtmlResponse) -> List[str]:
        return response.xpath('//section[@class="infoblock oeffnungszeiten"]/div/*/text()').getall()

    def parse_cinema(self, response: scrapy.http.response.html.HtmlResponse) -> dict:

        titles = self.get_titles(response)
        movies_times = [div.xpath('//table//td/text()').getall()
                        for div in response.css('div.table-responsive-wrapper')]

        cinema = Cinema(
            
            name=self.get_name(response),
            description=self.get_description(response),
            address=Address(street=self.get_street(response),
                            postal_code=self.get_postal_code(response),
                            district=self.get_district(response),
                            city='Berlin',
                            country='Germany'),
            contact=Contact(telephone=self.get_telephone(response)),
            prices=self.get_prices(response),

            shows=self.create_shows(titles, movies_times)
        )

        yield cinema.to_dict()
