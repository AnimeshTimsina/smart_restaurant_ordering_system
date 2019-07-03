from django.urls import path
from . import views_customer as views

urlpatterns = [
    path('index/',views.index,name='customerIndex'),


]
