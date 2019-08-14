from .models import Table,Food,Type,Profile,Category
from django.forms import ModelForm
from django.contrib.auth.models import User

class addTableForm(ModelForm):
    class Meta:
        model = Table
        fields = ['name','table_status']

    def save(self,commit=True):
        obj = super(addTableForm,self).save(commit=False)
        user = User.objects.create_user(obj.name,None,'password1234')
        user.save()
        obj.User = user
        obj.table_status = '3'
        if commit:
            obj.save()
        return obj

class addCategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

class addFoodForm(ModelForm):
    class Meta:
        model = Food
        fields = ['name','pricePerQuantity','type','description','imageUrl']

class addFoodTypeForm(ModelForm):
    class Meta:
        model = Type
        fields = "__all__"

class editTableForm(ModelForm):
    class Meta:
        model = Table
        fields = ['name','table_status']

class editProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

class editFoodForm(ModelForm):
    class Meta:
        model = Food
        fields = ['name','pricePerQuantity','type','description','imageUrl']

class editCategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
