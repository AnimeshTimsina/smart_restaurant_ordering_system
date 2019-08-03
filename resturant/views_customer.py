from django.shortcuts import render,HttpResponse,redirect
from .models import Table,Food
from django.contrib.auth.models import User
from django.contrib.auth import login

def table_allocate(request):
    table = Table.objects.all()
    context = {'table':table}
    return render(request,'customer/table_allocate.html',context)

def sessionBegin(request,table_name):
    table = Table.objects.get(name=table_name)
    user = table.User
    login(request,user)
    trending_foods = Food.objects.order_by('-orderCount')[:3]

    args = {'table_name':user,'trending_foods':trending_foods}
    return render(request,'customer/session.html',args)

def test_view(request):
    if 'data' in request.COOKIES:
        response = HttpResponse('Cookies found')
    else:
        response = HttpResponse('Cookies not found')
        response.set_cookie('data','confidential')
    return response

