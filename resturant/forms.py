from .models import Table
from django.forms import ModelForm
from django.contrib.auth.models import User

class addTableForm(ModelForm):
    class Meta:
        model = Table
        fields = ['name']

    def save(self,commit=True):
        obj = super(addTableForm,self).save(commit=False)
        user = User.objects.create_user(obj.name,None,'password1234')
        user.save()
        obj.User = user
        obj.table_status = '3'
        if commit:
            obj.save()
        return obj


        
        


    
    