from django.urls import path

from . import views

app_name = 'drive'
urlpatterns = [
    path('<path:path>', views.index),
]
