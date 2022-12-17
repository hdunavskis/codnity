from django.test import TestCase
from .models import Codnity
import datetime
from collections import namedtuple
from codnity.utils.db_utils import DBUtils
# from codnity.utils.scraper_threads import Scraper

class ScraperTestCase(TestCase):
    results = []
    Content = namedtuple('Content', 'title link points created')

    def setUp(self) -> None:
        Codnity.objects.create(
            title='codnity',
            link='www.codnity.com',
            points='4000 points',
            created=datetime.datetime(2023, 1, 1, 1, 00, 00)
            )

    def test_create_object(self):
        self.results.append([
        self.Content(
                title='test_title',
                link='test_link',
                points='600',
                created=datetime.datetime(2023, 2, 2, 2, 00, 00)
            )
        ])
        DBUtils.save_results(self.results)
        ob = Codnity.objects.get(title='test_title')
        self.assertEqual(ob.title, 'test_title')


    def test_update_object(self):
        self.results.append([
        self.Content(
                title='codnity',
                link='test_link',
                points='4500 points',
                created=datetime.datetime(2023, 1, 1, 1, 00, 00)
            )
        ])
        DBUtils.save_results(self.results)
        ob = Codnity.objects.get(title='codnity')
        self.assertEqual(ob.title, 'codnity')
        self.assertEqual(ob.points, '4500 points')
