import logging
import argparse
import requests
from . import codnity_logger

logger = logging.getLogger(__name__)


class Scraper:
    """Gets data from hacker news website"""
    def __init__(self, url:str):
        self.__url = url

    def __repr__(self) -> str:
        return f'Scraper(url={self.url})'

    def __str__(self) -> str:
        return self.__url

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        if not url:
            raise ValueError("Url is not provided!")
        self.__url = url


    @codnity_logger.Logger(logger=logger)
    def get_data(self):
        results = requests.get(self.url)
        return results.text

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    required_arguments = parser.add_argument_group('required named arguments')
    required_arguments.add_argument('-u', '--url', type=str,
    help='Website URL for scraping', required=True)
    args = parser.parse_args()

    if args.url is not None:
        scraper = Scraper(url=args.url)
        print('scraper', scraper.url)

if __name__ == '__main__':
    main()
