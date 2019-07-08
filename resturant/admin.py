from django.contrib import admin
from .models import Table,Type,Food,Customer,Orders
from django.contrib.auth.models import Group




admin.site.register(Table)
admin.site.register(Type)
admin.site.register(Food)
admin.site.register(Customer)
admin.site.register(Orders)
admin.site.unregister(Group)
