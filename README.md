# codnity
## Description
The project is to scrape data from 'hacker news' and store - "title, link, points, date created" values in database.  
This project includes two different web scraping approaches.
1. web scrape using asyncIO pythonon library (utils/scrape_asyncio.py)
2. web scrape using threadpool (utils/scrape_threads.py)  
*__The default web scrape approach is asyncIO. To switch to the threadpool web scraper you need to uncoment line: "from codnity.utils.scraper_threads import Scraper", and comment out "from codnity.utils.scraper_asyncio import Scraper" in two following files__*:  
  *- hacker_news/mangement/commands/web_scrape.py  
  *- hacker_news/views.py  

__All proxy IPs in this project are taken from a public website, and I dont have personal control over them. To increase the speed of execution add more and/or new proxy IPs to the list in the Scraper class. On the day all proxy IPs are working.__ 
### Requirements
Install and start Docker service

## Set up and execution
1. Download the project to your local environment
2. Locate into codnity directory where is *__"docker-compose.yaml"__* file
3. Run docker compose command to set up db and web containers:  
```docker-compose -f docker-compose.yaml up -d```  
4. Create super user. *__insert username, email and password__*:  
```docker-compose run web python manage.py createsuperuser```
5. To run the web scraper from a terminal:  
```docker-compose run web python manage.py web_scrape```
6. To run the web scraper from the website - press *"Update Results"* button.

#### Remove unused containers:  
```docker rm $(docker ps -a -f status=exited -q)```