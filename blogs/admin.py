from django.contrib import admin

from .models import Blog, Topic

# Register your models here.
admin.site.register(Topic)
admin.site.register(Blog)
