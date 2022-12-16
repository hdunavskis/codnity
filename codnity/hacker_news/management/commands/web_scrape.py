from django.core.management.base import BaseCommand
from codnity.utils.scraper import Scraper
import time
class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        start = time.time()
        Scraper().run_scraper()
        end = time.time()
        print('time', end-start)
        
