from django.urls import path
from . import views_customer as views

urlpatterns = [
    path('table_allocate/',views.table_allocate,name='table_allocate'),
    path('session/<int:table_id>',views.sessionBegin,name='sessionBegin'),


]
