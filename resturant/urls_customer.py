from django.urls import path
from . import views_customer as views

urlpatterns = [
    path('table_allocate/',views.table_allocate,name='table_allocate'),
    path('<str:table_name>/session',views.sessionBegin,name='sessionBegin'),
    path('test/',views.test_view,name='test_view'),
    path('food/<int:key>',views.food_details,name='food_details'),
    path('<str:table_name>/after_order',views.after_order,name='after_order'),
    path('<str:table_name>/pendingorders',views.pending_orders,name='pending_orders'),
    path('<str:table_name>/deletefood/<int:order_number>/<int:food_key>',views.delete_food_from_order,name='delete_food_from_order'),

]
