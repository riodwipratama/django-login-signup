from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 
from data_parameter import views
from upload_csv.views import upload_file_view
from deskriptif.views import getread
from data_parameter.models import data_produk


urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload-csv/', include('upload_csv.urls', namespace='csvs')),
    path('upload-csv/choose-file/', upload_file_view, name='csv_file'),
    path('signup/',views.signaction, name='signup'),
    path('index/',views.user_index, name='index'),
    path('',views.loginaction, name='user_login'),
    path('logout/',views.logout_request, name='user_logout'),
    path('user-profile/', views.user_profile, name='user-profile'),
    path('data-tabel-qc/', views.showDetails, name='data-tabel'),
    path('data-tabel-mesin/', views.data_tabel_mesin, name='data-tabel-mesin'),
    path('param-qc/',views.qc, name='param-qc'),
    path('param-mesin/', views.mesin, name='param-mesin'),
    path('deskriptif/', include('deskriptif.urls', namespace='deskriptif')),
    path('deskriptif-analysis/', getread, name='deskriptif'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)