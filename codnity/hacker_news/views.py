from django.views.generic import ListView
from typing import List
from .models import HackerNews
from codnity.utils.scraper import Scraper
from django.shortcuts import render

class HackerNewsView(ListView):
    model = HackerNews
    template_name: str = 'hacker_news/index.html'
    http_method_names: List = ['get']
    context_object_name: str = 'hacker_news'


def test(request):
    context = {}

    s = Scraper('https://news.ycombinator.com/news?p=5')

    context['results'] = s.get_data()

    return render(request, 'hacker_news/test.html', context)