from django.contrib import admin
from .models import Orders, Products

# Register your models here.
admin.site.register(Products)
admin.site.register(Orders)