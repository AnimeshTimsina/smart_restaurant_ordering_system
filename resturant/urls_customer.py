from django.urls import path
from . import views_customer as views

urlpatterns = [
    path('table_allocate/',views.table_allocate,name='table_allocate'),
    path('<str:table_name>/session',views.sessionBegin,name='sessionBegin'),
    path('test/',views.test_view,name='test_view'),
    


]
