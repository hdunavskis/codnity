from collections import namedtuple
import logging
from typing import List
import random
from datetime import datetime
import threading
from concurrent.futures import ThreadPoolExecutor
import httpx
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from codnity.utils.db_utils import DBUtils


logging.basicConfig(level=logging.DEBUG)

class Scraper:
    """Gets data from hacker news website"""
    
    _lock = threading.Lock()
    URL = 'https://news.ycombinator.com/news?p='
    PROXY_POOL = [
        'http://38.49.135.249:999',
        'http://173.212.224.134:3129',
        'http://34.175.45.228:3128',
        'http://208.79.10.113:9080',
        'http://20.239.27.216:3128',
        'http://20.121.184.238:443',
    ]
    UA = UserAgent()
    saved_data = []

    def __repr__(self) -> str:
        return f'Scraper(url={self.URL})'


    def __str__(self) -> str:
        return self.URL


    @property
    def url(self) -> str:
        return self.URL


    def run_scraper(self):
        with ThreadPoolExecutor(max_workers=4, thread_name_prefix='thread') as executor:
            executor.submit(Scraper._get_results)
            executor.submit(Scraper._get_results)
            executor.submit(Scraper._get_results)
            executor.submit(Scraper._get_results)
        DBUtils.save_results(self.saved_data)


    @staticmethod
    def _get_results() -> None:
        final_page = False
        index = 1
        while not final_page:
            try:
                with Scraper._lock:
                    web_content = Scraper._fetch_data(index)
                    index += 1
            except httpx.HTTPError as err:
                logging.error(err)
            else:
                soup = BeautifulSoup(web_content.text, 'html.parser')
                title_head = soup.find_all("span", class_="titleline")
                subtext = soup.find_all("td", class_="subtext")
                parsed_data = Scraper._parse_data(title_head, subtext)
                Scraper.saved_data.append(parsed_data)
                more_pages = soup.find('a', class_='morelink')

                if not more_pages:
                    final_page = True


    @staticmethod
    def _fetch_data(index):
        proxy = Scraper.PROXY_POOL[random.randint(0, len(Scraper.PROXY_POOL)-1)]
        with httpx.Client(proxies={'https://':proxy},
                                headers={'User-Agent':Scraper.UA.random}, timeout=2) as client:
            return client.get(Scraper.URL + str(index))


    @staticmethod
    def _parse_data(title_head, subtext)->List:
        results = []
        Content = namedtuple('Content', 'title link points created')

        titles_and_links = Scraper._get_title_and_link(title_head)
        points_and_dates = Scraper._get_points_and_date(subtext)
        for title_link, point_date in zip(titles_and_links, points_and_dates):
            results.append(
                Content(
                    title=title_link[0],
                    link=title_link[1],
                    created=point_date[1],
                    points=point_date[0],
                    ))
        return results


    @staticmethod
    def _get_points_and_date(subtext)->List:
        format_ = '%Y-%m-%dT%H:%M:%S'
        results = []
        for text in subtext:
            date_str = text.find('span', class_='age')['title']
            parsed_date = datetime.strptime(date_str, format_)
            points = text.find('span', class_='score')
            points = points.text if points else '0 points'
            results.append((points, parsed_date))
        return results


    @staticmethod
    def _get_title_and_link(title_head)->List:
        results = []
        for title in title_head:
            title_ = title.find('a').text
            link_ = title.find('a')['href']
            if str(link_).startswith('item?id='):
                link_ = 'https://news.ycombinator.com/'+str(link_)
            results.append((title_, link_))
        return results
   