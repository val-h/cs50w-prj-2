from django.contrib import admin

from .models import *

# Register your models here.

# Reconfigure
class WatchlistAdmin(admin.ModelAdmin):
    filter_horizontal = ("listings",)

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist, WatchlistAdmin)
