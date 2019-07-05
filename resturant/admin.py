from django.contrib import admin
from .models import Table,Type,Food,Customer,Orders,MyUser
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserCreationForm

class UserAdmin(BaseUserAdmin):
	add_form = UserCreationForm

	list_display = ('username','email','is_admin')
	list_filter = ('is_admin',)

	fieldsets = (
			(None, {'fields': ('username','email','password')}),
			('Permissions', {'fields': ('is_admin',)})
		)
	search_fields = ('username','email')
	ordering = ('username','email')

	filter_horizontal = ()
# Register your models here.

admin.site.register(MyUser, UserAdmin)
admin.site.register(Table)
admin.site.register(Type)
admin.site.register(Food)
admin.site.register(Customer)
admin.site.register(Orders)
admin.site.unregister(Group)
