from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^paypal/',include('paypal.standard.ipn.urls')),
    path('management/',include('resturant.urls_management')),
    path('customer/',include('resturant.urls_customer')),


] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
