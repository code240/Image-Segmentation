# import imp
from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Admindata)
admin.site.register(Article)
admin.site.register(Media)
admin.site.register(Segment)
