from django.shortcuts import render,HttpResponse,redirect
from .models import Table,Food,Orders,Customer,Rate,Recommended,Category,Type
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.http import HttpResponseRedirect
import turicreate as tc
import pandas as pd
from collections import defaultdict
import datetime
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt


def welcome2(request,table_name):
    r_cols = ['user_id','food_id','rating']
    ratings=pd.read_csv("rates.txt",sep='\t',names=r_cols,encoding='latin-1')

    i_cols=['food_id','food_title','Veg','Non-veg','soft','hard']
    items=pd.read_csv("food_info.txt",sep='|',names=i_cols,encoding='latin-1')

    n_users=ratings.user_id.unique().shape[0]
    n_items=ratings.food_id.unique().shape[0]

    train_data=tc.SFrame(ratings)
    item_data=tc.SFrame(items)

    #For new users

    session_id=request.COOKIES['restaurant_session_id']
    customer = Customer.objects.get(session_id = session_id)
    if not Rate.objects.filter(customer = customer).exists():
        print("New User")
        FactorizationRecommender=tc.recommender.popularity_recommender.create(train_data,user_id='user_id',item_id='food_id',target='rating',
                                                                        user_data=None,item_data=item_data,random_seed=0,verbose=True)
    else:
        print("Old user")
          #For items having ratings
        FactorizationRecommender=tc.recommender.factorization_recommender.create(train_data, user_id='user_id', item_id='food_id', target='rating', user_data=None, item_data=item_data, num_factors=8, regularization=1e-08, linear_regularization=1e-10, side_data_factorization=True, nmf=False, binary_target=False, max_iterations=50, sgd_step_size=0, random_seed=0, solver='auto')
    recommended_output=FactorizationRecommender.recommend(users=[customer.id],k=3)
    recommen=tc.SFrame(recommended_output)
    recommended_output=recommen["food_id"]
    id_list = []
    for i in recommended_output:
        id_list.append(i)
    print("Yaa cha:",id_list)
    recommended_output = id_list

    table = Table.objects.get(name=table_name)
    rec_table = Recommended.objects.filter(table = table)
    if rec_table.exists():
        rec_table = rec_table[0]
        rec_table.recommended_ids = recommended_output
        rec_table.save()
    else:
        rec_table = Recommended.objects.create(table = table,recommended_ids = recommended_output)

    return redirect('sessionBegin',table_name)



def table_allocate(request):
    table = Table.objects.all()
    context = {'table':table}
    return render(request,'customer/table_allocate.html',context)

def sessionBegin(request,table_name):
    table = Table.objects.get(name=table_name)
    user = table.User
    login(request,user)
    rec_table = Recommended.objects.filter(table = table)[0]
    recommended_output = rec_table.recommended_ids
    print("Yo ho saale",recommended_output)
    recommended_foods = Food.objects.none()
    for i in recommended_output:
        recommended_foods |= Food.objects.filter(id=i)
    trending_foods = Food.objects.order_by('-orderCount')[:3]
    args = {'table_name':user,'trending_foods':trending_foods,'recommended_foods':recommended_foods}
    response = render(request,'customer/session.html',args)
    return response
    # recommended = recommended_ids(request)
    # recommended_foods = Food.objects.none()
    # for i in recommended:
    #     recommended_foods |= Food.objects.filter(id=i)


def test_view(request):
    if 'data' in request.COOKIES:
        response = HttpResponse('Cookies found')
    else:
        response = HttpResponse('Cookies not found')
        response.set_cookie('data','confidential')
    return response

def food_details(request,table_name,key):
    selected_food = Food.objects.get(pk=key)
    if request.method == 'POST':
        number = int(request.POST['quantity'])
        tableObj = Table.objects.get(User = request.user)
        order = Orders.objects.filter(table = tableObj)
        order = order.filter(order_status = '1')
        if order.exists():
            order = order.first()
            count = 0
            found = False
            for food in order.food.all():
                if (food != selected_food):
                    count = count+1
                else:
                    order.quantity[count] += number
                    found = True
            if (found == False) :
                order.quantity.append(number)
        else:
            current_table = Table.objects.get(name = request.user.username)
            order = Orders(table = current_table)
            order.quantity.append(number)
            order.save()
        order.food.add(selected_food)
        order.save()
        return redirect('after_order',table_name = request.user.username)
    args = {'food':selected_food,'table_name':table_name}
    return render(request,'customer/food_details.html',args)

def after_order(request,table_name):
    return render(request,'customer/after_order.html',{'table_name':table_name})

def pending_orders(request,table_name):
    table = Table.objects.get(User = request.user)
    orders = Orders.objects.filter(table = table).filter(order_status = '1')
    try:
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

        print("Here1")
            # order_id = request.session.get('order_id')
        host = request.get_host()
        print("Here2")

            # What you want the button to do.
        paypal_dict = {
                "business": settings.PAYPAL_RECEIVER_EMAIL,
                # "amount": %.2f %order.get_total_cost().quantize(Decimal('.01')),
                'amount':totalCost,
                # "item_name": "name of the item",
                "invoice": order.id,
                "notify_url":'http://{}{}'.format(host,reverse('paypal-ipn')),
                "return_url":'http://{}{}'.format(host,reverse('after_payment' ,args=[ table_name ] )),
                "cancel_return":'http://{}{}'.format(host,reverse('cancelled',args=[table_name])),
                # "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
            }
        print(paypal_dict)
        print("Here3")
        

            # Create the instance.
        forms = PayPalPaymentsForm(initial=paypal_dict)
        args = {'orders':orders,'order':order_formatted,'totalCost':totalCost,'table_name':table_name,'form':forms}

    except:
        args = {'orders':orders,'table_name':table_name}
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
    if not order.food.all().exists():
        order.delete()

    print(food_to_delete,quantity_to_delete,cost_to_delete)
    return redirect('pending_orders',table_name = table_name)

@csrf_exempt
def after_payment(request,table_name):
    table = Table.objects.get(User = request.user)
    order = Orders.objects.filter(table = table).filter(order_status = '1')[0] #'1' means pending
    order.order_status = '2' #'2' means confirmed
    foods = order.food.all()
    for food in foods:
        food.orderCount+=1
        food.save()
    order.save()
    args = {'table_name':table_name}
    return render(request,'customer/after_payment.html',args)

@csrf_exempt
def cancelled(request,table_name):
    context ={'table_name':table_name}
    return render(request,'customer/cancelled.html')

def confirmed_orders(request,table_name):
    table = Table.objects.get(User = request.user)
    orders = Orders.objects.filter(table = table).filter(order_status = '2')

    args = {'orders':orders,'table_name':table_name}
    return render(request,'customer/confirmed_orders.html',args)

def confirmed_order_details(request,table_name,key):
    table = Table.objects.get(User=request.user)
    order = Orders.objects.get(pk=key)
    key = order.id
    print(key)
    try:
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
        args = {'eta':order.eta,'order':order_formatted,'totalCost':totalCost,'table_name':table_name,'key':key}
    except:
        args = {'eta':order.eta,'table_name':table_name,'key':key}
    return render(request,'customer/confirmed_order_details.html',args)

def rate(request,table_name):
    table = Table.objects.get(User=request.user)
    orders = Orders.objects.filter(table = table).filter(order_status = '2')
    foods = []
    for order in orders:
        for food in order.food.all():
            obj = Food.objects.get(pk = food.id)
            foods.append(obj)
    b = set()
    unique_foods = []
    for x in foods:
        if x not in b:
            unique_foods.append(x)
            b.add(x)
    args = {'foods':unique_foods}
    customer_exists = False
    response = render(request,'customer/rate.html',args)
    if request.method == "POST":
        if 'restaurant_session_id' in request.COOKIES:
            customer_exists = True
            customer_obj = Customer.objects.get(session_id=request.COOKIES['restaurant_session_id'])
        else:
            customer_obj = Customer.objects.create()

        for i in unique_foods:
            star = request.POST['stars_of_'+str(i.id)]
            food_obj = Food.objects.get(pk=i.id)
            rate_obj = Rate.objects.filter(customer = customer_obj).filter(food = food_obj)
            print(rate_obj)
            if rate_obj.exists():
                rate_obj = rate_obj[0]
                rate_obj.rating = int(star)
                rate_obj.save()
            else:
                Rate.objects.create(customer = customer_obj,food = food_obj, rating = int(star))
            current_table = Table.objects.get(User = request.user)
            orders = Orders.objects.filter(table = current_table)
            for order in orders:
                order.delete()
            response = render(request,'customer/thankyou.html',args)
            if (customer_exists == False):
                response.set_cookie('restaurant_session_id',customer_obj.session_id)
    return response

def bill(request,table_name):
    table = Table.objects.get(User = request.user)
    orders = Orders.objects.filter(table = table).filter(order_status = '2')
    foods = []
    quantities = []
    costs = []
    for order in orders:
        for food in order.food.all():
            foods.append(food)
        for q in order.quantity:
            quantities.append(q)
        for c in order.costList:
            costs.append(c)
    print(foods)
    print(quantities)
    print(costs)
    lt = list(zip(foods,costs))
    d = defaultdict(list)
    for k,v in lt:
        d[k].append(v)
    d = list(d.items())
    new_foods=[]
    for k in d:
        new_foods.append(k[0])
    co=[]
    a=0
    for i in d:
        for j in i[1]:
            a+=j
        co.append(a)
        a=0
    print(new_foods)
    print(co)
    individual_costs = []
    quantities = []
    for food in new_foods:
        individual_costs.append(food.pricePerQuantity)
    for i in range(len(co)):
        quantities.append(int(co[i]/individual_costs[i]))
    print(quantities)
    totalCost = 0
    for i in co:
        totalCost += i
    x = datetime.datetime.now()
    date = x.strftime("%x")
    final = []
    for i in range(len(quantities)):
        final.append([new_foods[i],quantities[i],co[i]])
    print(final)
    args = {'final':final,'totalCost':totalCost,'date':date,'table_name':table_name}
    # pdf = render_to_pdf('customer/bill.html', args)
    # return HttpResponse(pdf, content_type='application/pdf')
    return render(request,'customer/bill.html',args)

def welcome(request,table_name):
    args = {'table_name':table_name}
    response = render(request,'customer/welcome.html',args)
    customer_exists = False
    if 'restaurant_session_id' in request.COOKIES:
        customer_exists = True
        customer_obj = Customer.objects.get(session_id=request.COOKIES['restaurant_session_id'])
    else:
        customer_obj = Customer.objects.create()
    if (customer_exists == False):
        response.set_cookie('restaurant_session_id',customer_obj.session_id)
    return response

def menu(request,table_name):
    foods = Food.objects.all()
    category = Category.objects.all()
    return render(request,'customer/menu.html',{'foods':foods,'category':category,'table_name':table_name})

def items(request,table_name,key):
    foods = Food.objects.all()
    category = Category.objects.all()
    c = Category.objects.get(pk=key)
    f = c.foods.all()
    context={'foods':foods,'category':category,'f':f,'table_name':table_name}
    return render(request,'customer/items.html',context)
