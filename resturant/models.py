import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save
from datetime import datetime,timedelta
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.signals import user_logged_in
import turicreate as tc
import pandas as pd
from django.shortcuts import render,HttpResponse

# Create your models here.

class Profile(models.Model):
    type_choices = (
            ('1', 'manager'),
            ('2', 'waiter'),
        )
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    designation = models.CharField(max_length=1,choices = type_choices)
    contact_no = models.CharField(max_length = 12)
    address = models.CharField(max_length=50)
    image = models.ImageField(default='default.jpg',upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

class RestaurantInfo(models.Model):
    name = models.CharField(max_length=100, blank = True, null = True)
    service_tax = models.DecimalField(max_digits=10, decimal_places = 5, default = 0)
    description = models.CharField(max_length=1000, blank = True, null = True)

    def __str__(self):
        return self.name



class Table(models.Model):
    User = models.OneToOneField(User, verbose_name=("linked_user"), on_delete=models.CASCADE, related_name = 'current_table')
    type_choices = (
        ('1', 'booked'),
        ('2', 'reserved'),
        ('3', 'free'),
    )
    name = models.CharField(max_length=50, blank = True, null = True)
    table_status = models.CharField(max_length=1, choices=type_choices)

    def __str__(self):
        return self.name

@receiver(post_save, sender=Table)
def _post_save_receiver(sender,instance,created, **kwargs):
    if created:
        instance.name = instance.User.username
        instance.save()

class Category(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name

class Type(models.Model):
    type_name = models.CharField(max_length=50)

    def __str__(self):
        return self.type_name

class Food(models.Model):
    name = models.CharField(max_length=50)
    pricePerQuantity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='foods')
    type = models.ForeignKey(Type,on_delete=models.CASCADE,related_name='foods')
    rating = JSONField(null=True,blank=True)
    orderCount = models.IntegerField(default=0)
    description = models.CharField(max_length=5000)
    imageUrl = models.URLField(null=True,blank=True)


    def __str__(self):
        return self.name

class Customer(models.Model):
    session_id = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return str(self.session_id);


class Orders(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    food = models.ManyToManyField(Food)
    quantity = ArrayField(models.IntegerField(),default=list)
    dateOfCreation = models.DateTimeField(auto_now_add=True)
    costList = ArrayField(models.IntegerField(),blank=True,default=list)
    totalCost = models.IntegerField(default=0)
    options =  (
        ('1', 'pending'),
        ('2', 'confirmed'),
    )
    order_status = models.CharField(max_length=1, choices=options,default = '1')
    eta = models.CharField(default=0,null=True,blank=True,max_length=3)

    def __str__(self):
        return str(str(self.table) + str(self.id))

    def get_eta_in_seconds(self):
        return (float(self.eta)/60)

class Rate(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    food = models.ForeignKey(Food,on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(blank=True,null=True, validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        response = str(self.customer) + "-" + str(self.food)
        return response

@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save,sender=User)
def save_profile(sender,instance,**kwargs):
    instance.profile.save()

@receiver(post_save,sender=Rate)
def write_to_file(sender,instance,created,**kwargs):
    if created:
        text = str(instance.customer.id) + "\t" + str(instance.food.id) + "\t" + str(instance.rating) + "\n"
        print(text)
        f = open("rates.txt", "a")
        f.write(text)
        f.close()



class Recommended(models.Model):
    table = models.ForeignKey(Table,on_delete=models.CASCADE)
    recommended_ids = ArrayField(models.IntegerField(),blank=True,default=list)

    def __str__(self):
        return self.table.name

@receiver(post_save,sender = Food)
def write_to_file(sender,instance,created,**kwargs):
    text = ''
    if created:
        text = text + str(instance.pk)+ '\t'+ str(instance.name)+"\t"
        for i in Type.objects.all():
            if instance.type == i:
                text = text + str(1) +'\t'
            else:
                text = text + str(0) + "\t"
        text = text + "\n"
        f=open("food_info.txt","a")
        f.write(text)
        f.close()
