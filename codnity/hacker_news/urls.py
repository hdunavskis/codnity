from django.urls import path
from . import views

urlpatterns = [
    # path('', views.HackerNewsView.as_view(), name='hacker_news'),
    path('', views.test, name='hacker_news'),
]
