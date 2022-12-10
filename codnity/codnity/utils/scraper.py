import argparse
import requests
from bs4 import BeautifulSoup

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

    def scrape_web(self):
        self._run_scraper()

    def _run_scraper(self):
        content = self._get_page_content
        soup = BeautifulSoup(content.content, 'html.parser')
        titles = self._get_title(soup)

    def _get_page_content(self):
        return requests.get(self.url)

    def _get_title(self, soup):
       #title_head = soup.find_all("span", class_="titleline")
       #href = title_head[0].find('a')
       #subline = soup.find_all("span", class_="subline")
       #title =  subline[0].find('span', class_'age')['title']
       #points =  subline[0].find('span', class_'score')
       #points = points.text
        titles = soup.find_all("span", class_="titleline")


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
