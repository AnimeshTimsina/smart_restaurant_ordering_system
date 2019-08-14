from django.contrib import admin
from .models import Table,Type,Food,Customer,Orders,Category,RestaurantInfo,Profile,Rate,Recommended
from django.contrib.auth.models import Group




admin.site.register(Table)
admin.site.register(Type)
admin.site.register(Food)
admin.site.register(Customer)
admin.site.register(Orders)
admin.site.register(Category)
admin.site.register(RestaurantInfo)
admin.site.register(Rate)
admin.site.register(Recommended)
admin.site.unregister(Group)
admin.site.register(Profile)
