from django.contrib import admin
from .models import *

#class ObjectAdmin(admin.ModelAdmin):

admin.site.register(Category)
admin.site.register(Object)
admin.site.register(Choice)
