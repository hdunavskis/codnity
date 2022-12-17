from collections import namedtuple
import logging
from typing import List
import random
from datetime import datetime
import asyncio
import httpx
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from codnity.utils.db_utils import DBUtils

logging.basicConfig(level=logging.DEBUG)

class Scraper:
    """Gets data from hacker news website"""

    URL = 'https://news.ycombinator.com/news?p='
    PROXY_POOL = [
        'http://38.49.135.249:999',
        'http://173.212.224.134:3129',
        'http://34.175.45.228:3128',
        'http://208.79.10.113:9080',
        'http://20.239.27.216:3128',
        'http://20.121.184.238:443',
        'http://135.148.95.28:3128'
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
        asyncio.run(Scraper._get_results())
        DBUtils.save_results(self.saved_data)


    @staticmethod
    async def _get_results() -> None:
        index = 1
        final_page = False
        while not final_page:
            try:
                web_content = await Scraper._fetch_data(index)
            except httpx.HTTPError:
                index -= 1
            else:
                soup = BeautifulSoup(web_content.text, 'html.parser')
                title_head = soup.find_all("span", class_="titleline")
                subtext = soup.find_all("td", class_="subtext")
                parsed_data = await Scraper._parse_data(title_head, subtext)
                Scraper.saved_data.append(parsed_data)
                more_pages = soup.find('a', class_='morelink')

                if not more_pages:
                    final_page = True
            index += 1


    @staticmethod
    async def _fetch_data(index):
        proxy = Scraper.PROXY_POOL[random.randint(0, len(Scraper.PROXY_POOL)-1)]
        async with httpx.AsyncClient(proxies={'https://':proxy},
                                headers={'User-Agent':Scraper.UA.random}, timeout=1) as client:
            return await client.get(Scraper.URL + str(index))


    @staticmethod
    async def _parse_data(title_head, subtext)->List:
        results = []
        Content = namedtuple('Content', 'title link points created')

        titles_and_links, points_and_dates = await asyncio.gather(
            Scraper._get_title_and_link(title_head),
            Scraper._get_points_and_date(subtext)
        )

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
    async def _get_points_and_date(subtext)->List:
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
    async def _get_title_and_link(title_head)->List:
        results = []
        for title in title_head:
            title_ = title.find('a').text
            link_ = title.find('a')['href']
            if str(link_).startswith('item?id='):
                link_ = 'https://news.ycombinator.com/'+str(link_)
            results.append((title_, link_))
        return results
   