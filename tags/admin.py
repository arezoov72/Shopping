from django.contrib import admin
from .models import Tag

# Register your models here.

@admin.register(Tag)
class Tagadmin(admin.ModelAdmin):
    search_fields=['lable']