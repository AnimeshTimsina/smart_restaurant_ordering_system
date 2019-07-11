from django.shortcuts import render, redirect
from django.dispatch import receiver, Signal
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Orders
from django.db.models.signals import m2m_changed
from .forms import addTableForm

new_order_created = Signal(providing_args = ['table','food','quantity','dateOfCreation','costList','arrived','paid','id'])

def index(request):
    obj = Orders.objects.latest('dateOfCreation')
    print(obj)
    return render(request,'management/managementIndex.html')

def track_orders(request):
    context = {}
    return render(request,'management/track_orders.html',context)

def broadcast_to_socket(instance):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
       
        "order_track",{
        'type':'broadcast',
        'table':str(instance.table),
        'food':getFood(instance),
        'quantity':str(instance.quantity),
        'dateOfCreation':str(instance.dateOfCreation),
        'costList':str(instance.costList),
        'totalCost':str(instance.totalCost),
        'arrived':str(instance.arrived),
        'paid':str(instance.paid),
        'id':str(instance.id)
        })



def getFood(instance,**kwargs):
    foodDict = []
    for i in instance.food.all():
        foodDict.append(str(i))
    temp =str(foodDict)
    return temp[1:-1]
    

def newOrderCreated(sender,instance,action,**kwargs):
        if (action == "post_add"):
                cost = 0
                count = 0
                for i in instance.food.all():
                        instance.costList.append(i.pricePerQuantity * instance.quantity[count])
                        cost = cost + (i.pricePerQuantity * instance.quantity[count])
                        count = count + 1
                instance.totalCost = cost
                instance.save()
                broadcast_to_socket(instance)
 
m2m_changed.connect(newOrderCreated,sender=Orders.food.through)

def addTable(request):
        if request.method=="POST":
                form = addTableForm(request.POST)
                if form.is_valid():
                        form.save()
                        return redirect('addTable')
        else:
                form=addTableForm()
        args = {'form':form}
        return render(request,'management/addTable.html',args)



