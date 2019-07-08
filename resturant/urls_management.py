from django.urls import path
from . import views_management as views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('index/',views.index,name='managementIndex'),
    path('', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),

]
