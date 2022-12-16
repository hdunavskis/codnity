from django.contrib import admin
from .models import Codnity


@admin.register(Codnity)
class CodnityAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'points', 'created')
