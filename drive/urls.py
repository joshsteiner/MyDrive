from django.urls import path

from . import views

app_name = 'drive'
urlpatterns = [
    path('', views.root, name='root'),
    path('<path:path>', views.index, name='index'),
]
