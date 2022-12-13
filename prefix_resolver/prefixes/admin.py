from django.contrib import admin

from .models import IPv4prefix

class IPv4Admin(admin.ModelAdmin):

    list_display = ('prefix', 'nexthop', 'metric', )
    search_fields = ('prefix',)
    list_filter = ('prefix',)
    empty_value_display = '-пусто-'

admin.site.register(IPv4prefix, IPv4Admin)