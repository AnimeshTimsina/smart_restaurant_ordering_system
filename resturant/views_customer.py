from django.shortcuts import render,HttpResponse,redirect
from .models import Table,Food,Orders
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import HttpResponseRedirect

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

def food_details(request,key):
    selected_food = Food.objects.get(pk=key)
    if request.method == 'POST':
        number = int(request.POST['quantity'])
        tableObj = Table.objects.get(User = request.user) 
        order = Orders.objects.filter(table = tableObj)
        order = order.filter(order_status = '1')
        if order.exists():
            order = order.first()
            order.quantity.append(number)
        else:
            current_table = Table.objects.get(name = request.user.username)
            order = Orders(table = current_table)
            order.quantity.append(number)
            order.save()
        order.food.add(selected_food)
        order.save()
        return redirect('after_order',table_name = request.user.username)
    args = {'food':selected_food}
    return render(request,'customer/food_details.html',args)

def after_order(request,table_name):
    return render(request,'customer/after_order.html',{'table_name':table_name})

def pending_orders(request,table_name):
    table = Table.objects.get(User = request.user)
    orders = Orders.objects.filter(table = table).filter(order_status = '1')
    order = orders[0]
    order_formatted = []
    foods = order.food.all()
    quantities = order.quantity
    costs = order.costList
    totalCost = order.totalCost
    eta = order.eta
    count = 0
    for i in foods:
        order_formatted.append(
            [
                foods[count].name,
                quantities[count],
                costs[count]
            ]
        )
        count = count+1

    args = {'orders':orders,'order':order_formatted,'totalCost':totalCost,'table_name':table_name}
    return render(request,'customer/pending_orders.html',args)

def delete_food_from_order(request,table_name,order_number,food_key):
    order = Orders.objects.get(pk=order_number)
    food_to_delete = order.food.all()[food_key]
    quantity_to_delete = order.quantity[food_key]
    cost_to_delete = order.costList[food_key]
    #remove the required food, quantity and cost from order object and calculate total cost accordingly
    order.food.remove(food_to_delete)
    order.quantity.remove(quantity_to_delete)
    order.costList.remove(cost_to_delete)
    order.totalCost -= cost_to_delete
    order.save()
    print(food_to_delete,quantity_to_delete,cost_to_delete)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def after_payment(request,table_name):
    table = Table.objects.get(User = request.user)
    order = Orders.objects.filter(table = table).filter(order_status = '1')[0] #'1' means pending
    order.order_status = '2' #'2' means confirmed
    order.save()
    args = {'table_name':table_name}
    return render(request,'customer/after_payment.html',args)
