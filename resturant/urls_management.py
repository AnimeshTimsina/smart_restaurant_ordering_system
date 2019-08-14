from django.urls import path
from . import views_management as views
from django.contrib.auth import views as auth_views
from . import views_authentication as authenticate_views

urlpatterns = [
    path('index/',views.index,name='managementIndex'),
    path('', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('trackOrders/',views.track_orders,name='track_orders'),
    path('addTable/',views.addTable,name='addTable'),
    path('addFood/',views.addFood,name='addFood'),
    path('addCategory/',views.addCategory,name='addCategory'),
    path('addFoodType/',views.addFoodType,name='addFoodType'),
    path('register/', authenticate_views.register, name='register'),
    path('profile/',authenticate_views.view_profile,name="profile"),
    path('editProfile/<int:key>',authenticate_views.editProfile,name="editProfile"),
    path('tableView/',views.viewTable,name='viewTable'),
    path('editTable/<int:key>/',views.editTable,name='editTable'),
    path('deleteTable/<int:key>/',views.deleteTable,name='deleteTable'),
    path('about/',views.about,name='about'),
    path('changePassword/',authenticate_views.changePassword,name='change_password'),
    path('tableView/',views.viewTable,name='viewTable'),
    path('viewMenu/',views.viewMenu,name='viewMenu'),
    path('viewFood/<int:key>',views.viewFood,name='viewFood'),
    path('editFood/<int:key>',views.editFood,name='editFood'),
    path('deleteFood/<int:key>',views.deleteFood,name='deleteFood'),
    path('editCategory/<int:key>',views.editCategory,name='editCategory'),
    path('deleteCategory/<int:key>',views.deleteCategory,name='deleteCategory'),
    path('confirmedorders/',views.confirmed_orders,name='confirmed_orders'),
    path('seteta/<int:key>',views.set_eta,name="set_eta"),
]
