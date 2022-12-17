from django.views.generic import ListView
from typing import List
from .models import Codnity
from codnity.utils.scraper_asyncio import Scraper
# from codnity.utils.scraper_threads import Scraper
from django.shortcuts import redirect
from django.urls import reverse


class HackerNewsView(ListView):
    model = Codnity
    template_name: str = 'hacker_news/index.html'
    http_method_names: List = ['get']
    context_object_name: str = 'hacker_news'


def update_results(request):
    Scraper().run_scraper()
    return redirect(reverse('hacker:hacker_news'))
