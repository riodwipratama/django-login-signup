from django.contrib import admin
from data_parameter.models import getempdetails
from .models import data_produk

# Register your models here.
@admin.register(getempdetails)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("empname", "job", "email", "username", "password")

@admin.register(data_produk)
class DataRegistered(admin.ModelAdmin):
    list_display = ("product", "unit", "kelembaban", "tekanan", "waktu", "suhu", "sudut")
    