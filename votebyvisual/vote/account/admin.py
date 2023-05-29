from django.contrib import admin
from .models import *
# Register your models here.

class AdminPhoto(admin.ModelAdmin):
    list_display = ['caption', 'image']
