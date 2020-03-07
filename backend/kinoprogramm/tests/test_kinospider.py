
import unittest
from datetime import datetime

from spiders.data_structures import Show
from spiders.kinoprogramm import KinoSpider


class TestKinoSpider(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.spider = KinoSpider()

    def test_create_shows(self):
        movies_times = [['So, 06.10.19: ', '20:30, 23:00', 'Mi, 09.10.19: ', '20:15'],
                        ['Mi, 09.10.19: ', '18:00', 'So, 06.10.19: ', '14:30',
                         'Mo, 07.10.19: ', '21:15']]
        titles = ['One movie', 'another movie']

        actual = self.spider.create_shows(titles, movies_times)

        expected = [Show('One movie', [datetime(2019, 10, 6, 20, 30),
                                       datetime(2019, 10, 6, 23, 00),
                                       datetime(2019, 10, 9, 20, 15),
                                       ]),
                    Show('another movie', [datetime(2019, 10, 9, 18, 00),
                                           datetime(2019, 10, 6, 14, 30),
                                           datetime(2019, 10, 7, 21, 15),
                                           ]),
                    ]

        self.assertEqual(actual, expected, 'failed to create movie shows')
