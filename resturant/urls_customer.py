from django.urls import path
from . import views_customer as views

urlpatterns = [
    path('table_allocate/',views.table_allocate,name='table_allocate'),
    path('<str:table_name>/session',views.sessionBegin,name='sessionBegin'),
    path('<str:table_name>/food/<int:key>',views.food_details,name='food_details'),
    path('<str:table_name>/after_order',views.after_order,name='after_order'),
    path('<str:table_name>/pendingorders',views.pending_orders,name='pending_orders'),
    path('<str:table_name>/deletefood/<int:order_number>/<int:food_key>',views.delete_food_from_order,name='delete_food_from_order'),
    path('<str:table_name>/paymentsuccess',views.after_payment,name='after_payment'),
    path('<str:table_name>/confirmedorders',views.confirmed_orders,name='confirmed_orders'),
    path('<str:table_name>/confirmedorders',views.confirmed_orders,name='confirmed_orders'),
    path('<str:table_name>/confirmedorders/<int:key>',views.confirmed_order_details,name='confirmed_order_details'),
    path('<str:table_name>/rate',views.rate,name='rate'),
    path('<str:table_name>/bill',views.bill,name='bill'),
    path('<str:table_name>/welcome',views.welcome,name='welcome'),
    path('<str:table_name>/welcome2',views.welcome2,name='welcome2'),
        path('<str:table_name>/menu/',views.menu,name='menu'),
    path('<str:table_name>/itemslist/<int:key>',views.items,name="items"),
    path('<str:table_name>/cancelled',views.cancelled,name='cancelled'),
]
