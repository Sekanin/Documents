from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'myapp'

urlpatterns = [
    path('', views.open_folder, name='open_folder'),
    path('folder/<str:folder_name>/', views.folder_view, name='folder_view'),
    path('folder/<str:folder_name>/file/<path:subfolder_names>/', views.dynamic_subfolder_view, name='dynamic_subfolder_view'),
    path('folder/<str:folder_name>/<str:file_name>/', views.open_files, name='open_files'),
    path('folder/<str:folder_name>/<path:subfolder_names>/<str:file_name>/', views.open_file, name='open_file'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
