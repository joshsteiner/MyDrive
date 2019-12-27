from django.urls import path

from . import views

app_name = 'drive'
urlpatterns = [
    path('fsop', views.file_system_op, name='fsop'),
    path('d/', views.root, name='root'),
    path('d/<path:path>', views.index, name='index'),
]
