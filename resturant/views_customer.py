from django.shortcuts import render
from .models import Table
from django.contrib.auth.models import User
from django.contrib.auth import login

def table_allocate(request):
    table = Table.objects.all()
    context = {'table':table}
    return render(request,'customer/table_allocate.html',context)

def sessionBegin(request,table_id):
    table = Table.objects.get(pk=table_id)
    user = table.User
    login(request,user)
    context = {'table_name':user}   
    return render(request,'customer/session.html',context)
