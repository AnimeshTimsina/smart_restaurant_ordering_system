from django.contrib import admin
from django.conf.urls import url
from django.urls import path,include
from resturant.views_authentication import register, login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('management/',include('resturant.urls_management')),
    path('customer/',include('resturant.urls_customer')),
    url(r'^register/$', register),
    url(r'^login/$', login_view),
    url(r'^logout/$', logout_view),
]
