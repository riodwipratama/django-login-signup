from django.contrib import admin
from .models import Csv
# Register your models here.

@admin.register(Csv)
class CsvFile(admin.ModelAdmin):
    list_display = ("file_name", "uploaded", "activated")