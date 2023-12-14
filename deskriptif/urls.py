from django.urls import path
from . import views

app_name = 'deskriptif'

urlpatterns = [
    path('', views.deskriptif_page, name="deskriptif")
]