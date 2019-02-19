from django.urls import path
from . import views

urlpatterns = [
    path('yuebao',views.yuebao),
    path('download',views.download_file)
]
