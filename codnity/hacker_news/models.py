from django.db import models

class Codnity(models.Model):
    title = models.TextField(blank=False, max_length=500)
    link = models.URLField(max_length=200)
    points = models.CharField(max_length=100)
    created = models.DateTimeField(max_length=100)

    class Meta:
        verbose_name_plural = "Codnity"

    def __str__(self):
        return str(self.title)
