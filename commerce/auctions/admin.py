from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, List, WatchList, Bid, Comment



admin.site.register(User,UserAdmin)

admin.site.register(List)

admin.site.register(WatchList)

admin.site.register(Bid)

admin.site.register(Comment)

