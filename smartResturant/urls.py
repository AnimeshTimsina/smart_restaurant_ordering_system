from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('management/',include('resturant.urls_management')),
    path('customer/',include('resturant.urls_customer')),
    

]
