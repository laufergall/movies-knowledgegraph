import scrapy


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

    def parse(self, response):

        selectors = response.xpath('//div[@class="controls"]/select/option')

        hrefs = ['https://www.berlin.de/kino/_bin/kinodetail.php/' + sel.attrib['value']
                 for sel in selectors if self.is_positiveinteger(sel.attrib['value'])]

        for href in hrefs:
            yield response.follow(href, self.parse_cinema)

    def parse_cinema(self, response):
        yield {
            'title': response.css("title::text").getall(),
        }
