from django.contrib import admin

# Register your models here.
from .models import Webtoon, User_Webtoon

admin.site.register(Webtoon)
admin.site.register(User_Webtoon)