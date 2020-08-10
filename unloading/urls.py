from unloading import views

from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('unload', views.unload, name='unload'),
]
