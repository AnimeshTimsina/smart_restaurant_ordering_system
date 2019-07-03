from django.urls import path
from . import views_management as views

urlpatterns = [
    path('index/',views.index,name='managementIndex'),


]
