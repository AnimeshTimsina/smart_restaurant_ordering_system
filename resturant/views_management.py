from django.shortcuts import render, redirect
from django.dispatch import receiver, Signal
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Orders,Category,Type,Food
from django.db.models.signals import m2m_changed,post_save
from .forms import addTableForm,addFoodForm,addFoodTypeForm,editTableForm,editFoodForm,editCategoryForm,addCategoryForm
from .models import Table
from django.contrib import messages
new_order_created = Signal(providing_args = ['table','food','quantity','dateOfCreation','costList','arrived','paid','id'])

def index(request):
    # obj = Orders.objects.latest('dateOfCreation')
    # print(obj)
    user = request.user.username
    context = {'user':user }
    return render(request,'management/restaurantmanagement.html',context)

def track_orders(request):
    tables = Table.objects.all()
    context = {'tables':tables}
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
        'order_status':str(instance.order_status),
        'id':str(instance.table.id)

        })

def viewTable(request):
    tables = Table.objects.all().order_by('name')
    context = {'table':tables}
    return render(request,'management/table.html',context)

def about(request):
    return render(request,'management/about.html')

def viewMenu(request):
    category = Category.objects.all().order_by('category_name')
    type = Type.objects.all().order_by('type_name')
    food = Food.objects.all().order_by('type')
    context = {'category':category,'type':type,'food':food}
    return render(request,'management/menu.html',context)


def viewFood(request,key):
    category = Category.objects.all().order_by('category_name')
    type = Type.objects.all().order_by('type_name')
    food = Food.objects.all().order_by('type')
    fooditem = Food.objects.get(id = key)
    context = {'f':fooditem,'category':category,'type':type,'food':food}
    return render(request,'management/food.html',context)

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
                print(instance.quantity)
                instance.costList = []
                for i in instance.food.all():
                        instance.costList.append(i.pricePerQuantity * int(instance.quantity[count]))
                        cost = cost + (i.pricePerQuantity * int(instance.quantity[count]))
                        count = count + 1
                instance.totalCost = cost
                instance.save()



def orderConfirmed(sender,instance,created,**kwargs):
        if (instance.order_status == '2'):
                broadcast_to_socket(instance)


m2m_changed.connect(newOrderCreated,sender=Orders.food.through)
post_save.connect(orderConfirmed,sender=Orders)

def editFood(request,key):
    obj = Food.objects.get(pk=key)
    if request.method=='POST':
        form = editFoodForm(request.POST,instance=obj)
        if form.is_valid:
            form.save()
            messages.success(request, f'Food Item updated successfully!')
            return redirect('viewMenu')
        else:
            messages.warning(request, f'Invalid input')
    else:
        form = editFoodForm(instance=obj)
    args = {'form':form}
    return render(request,'management/editFood.html',args)

def editCategory(request,key):
    obj = Category.objects.get(pk=key)
    if request.method=='POST':
        form = editCategoryForm(request.POST,instance=obj)
        if form.is_valid:
            form.save()
            messages.success(request, f'Food Category updated successfully!')
            return redirect('viewMenu')
        else:
            messages.warning(request, f'Invalid input')
    else:
        form = editCategoryForm(instance=obj)
    args = {'form':form}
    return render(request,'management/editCategory.html',args)



def editTable(request,key):
    obj = Table.objects.get(pk=key)
    if request.method=='POST':
        form = editTableForm(request.POST,instance=obj)
        if form.is_valid:
            form.save()
            messages.success(request, f'Table updated successfully!')
            return redirect('viewTable')
        else:
            messages.warning(request, f'Invalid input')
    else:
        form = editTableForm(instance=obj)
    args = {'form':form}
    return render(request,'management/editTable.html',args)

def deleteFood(request,key):
    if request.method == 'POST':
        try:
            Food.objects.get(pk = key).delete()
            messages.success(request, f'Food deleted successfully!')
        except:
            messages.warning(request, f'Unable to delete the food!')
        return redirect('viewMenu')
    return render(request,'management/deleteFood.html',{'food':Food.objects.get(pk=key)})

def deleteCategory(request,key):
    if request.method == 'POST':
        try:
            Category.objects.get(pk = key).delete()
            messages.success(request, f'Category deleted successfully!')
        except:
            messages.warning(request, f'Unable to delete the category!')
        return redirect('viewMenu')
    return render(request,'management/deleteFood.html',{'category':Category.objects.get(pk=key)})

def deleteTable(request,key):
    if request.method == 'POST':
        try:
            Table.objects.get(pk = key).delete()
            messages.success(request, f'Food deleted successfully!')
        except:
            messages.warning(request, f'Unable to delete the food!')
        return redirect('viewTable')
    return render(request,'management/deleteTable.html',{'table':Table.objects.get(pk=key)})


def addTable(request):
        if request.method=="POST":
                form = addTableForm(request.POST)
                if form.is_valid():
                        form.save()
                        return redirect('viewTable')
        else:
                form=addTableForm()
        args = {'form':form}
        return render(request,'management/addTable.html',args)

def addFood(request):
        if request.method=="POST":
                form = addFoodForm(request.POST)
                if form.is_valid():
                        form.save()
                        return redirect('managementIndex')
        else:
                form=addFoodForm()
        args = {'form':form}
        return render(request,'management/addFood.html',args)

def addCategory(request):
        if request.method=="POST":
                form = addCategoryForm(request.POST)
                if form.is_valid():
                        form.save()
                        return redirect('managementIndex')
        else:
                form=addCategoryForm()
        args = {'form':form}
        return render(request,'management/addCategory.html',args)

def addFoodType(request):
        if request.method=="POST":
                form = addFoodTypeForm(request.POST)
                if form.is_valid():
                        form.save()
                        return redirect('managementIndex')
        else:
                form=addFoodTypeForm()
        args = {'form':form}
        return render(request,'management/addFoodType.html',args)

def confirmed_orders(request):
        orders = Orders.objects.filter(order_status = '2')
        args={'orders':orders}
        return render(request,'management/confirmed_orders.html',args)

def set_eta(request,key):
        order = Orders.objects.get(pk=key)
        if request.method == "POST":
                eta = request.POST['eta']
                order.eta = eta
                order.save()
                return redirect('confirmed_orders')
        return render(request,'management/seteta.html',{'order':order})

def testView(request):
    text=""
    for i in Food.objects.order_by("id"):
            text = text + str(i.pk) + "|"+ str(i.name)
            for j in Type.objects.all():
                if i.type == j:
                    text = text +"|"+ str(1)
                else:
                    text = text + "|"+str(0)
            text = text + "\n"
    print(text)
    f = open("abc.csv","a")
    f.write(text)
    f.close()
    return HttpResponse("This is the test")                
