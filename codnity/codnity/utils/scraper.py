from collections import namedtuple
import logging
from typing import List
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from hacker_news.models import Codnity
from datetime import datetime
import httpx
import asyncio
import time
import random
import sys


logging.basicConfig(level=logging.DEBUG)

class Scraper:
    """Gets data from hacker news website"""
    URL = 'https://news.ycombinator.com/news?p='
    PROXY_POOL = [
        'http://38.49.135.249:999',
        'http://20.239.27.216:3128',
        'http://173.212.224.134:3129', # slow
        'http://34.175.45.228:3128',
        'http://208.79.10.113:9080',
        'http://38.49.135.249:999',
        'http://20.239.27.216:3128',
        'http://20.121.184.238:443',
        'http://135.148.95.28:3128'
    ]
    UA = UserAgent()
    Content = namedtuple('Content', 'title link created points')
    DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S'


    def __repr__(self) -> str:
        return f'Scraper(url={self.URL})'


    def __str__(self) -> str:
        return self.URL


    @property
    def url(self) -> str:
        return self.URL


    def run_scraper(self, index=None, saved_data=None) -> None:
        index = index or 1
        final_page = False
        saved_data = saved_data or []

        while not final_page:
            proxy = self.PROXY_POOL[random.randint(0, len(self.PROXY_POOL)-1)]
            try:
                with httpx.Client(proxies={'https://':proxy},
                                headers={'User-Agent':self.UA.random}, timeout=5) as client:
                    web_content = client.get(self.URL + str(index))
            except httpx.HTTPError:
                self.run_scraper(index, saved_data=saved_data)
            else:
                if web_content.is_error:
                    self.run_scraper(index, saved_data=saved_data)
                else:
                    soup = BeautifulSoup(web_content.text, 'html.parser')
                    title_head = soup.find_all("span", class_="titleline")
                    title = title_head[0].find('a').text
                    link = title_head[0].find('a')['href']
                    subline = soup.find_all("span", class_="subline")
                    date_str =  subline[0].find('span', class_='age')['title']
                    points =  subline[0].find('span', class_='score').text
                    created = datetime.strptime(date_str, self.DATE_TIME_FORMAT).utcnow()
                    saved_data.append(self.Content(title, link, created, points))
                    more_pages = soup.find('a', class_='morelink')
                    if not more_pages:
                        final_page = True
            index += 1
        self.save_results(saved_data)
        sys.exit(0)


    def save_results(self, save_data:List) -> None:
        for data in save_data:
            _, created = Codnity.objects.update_or_create(
                title=data.title,
                defaults={
                    'title':data.title,
                    'link':data.link,
                    'points':data.points,
                    'created':data.created
                    }
            )
            if not created:
                logging.error('Failed to save to db %s', data)
