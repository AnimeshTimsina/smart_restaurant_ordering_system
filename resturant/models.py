import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save
from datetime import datetime,timedelta

# Create your models here.
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
    session_id = models.UUIDField(primary_key = True, default=uuid.uuid4, editable=False)

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
    eta = models.DurationField(default = timedelta(seconds = 0))
    
    def __str__(self):
        return str(str(self.table) + str(self.id))

