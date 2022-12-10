from django.db import models

class HackerNews(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(null=True)
    link = models.URLField(max_length=200)
    points = models.IntegerField()
    created = models.DateTimeField()
