from django.urls import path
from . import views

app_name='hacker'
urlpatterns = [
    path('', views.HackerNewsView.as_view(), name='hacker_news'),
    path('update_results', views.update_results, name='update_results')

]
