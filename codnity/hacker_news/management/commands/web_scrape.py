from django.core.management.base import BaseCommand
from codnity.utils.scraper_asyncio import Scraper
# from codnity.utils.scraper_asyncio import Scraper

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Scraper().run_scraper()
