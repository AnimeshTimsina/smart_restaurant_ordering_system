from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.contrib.auth.models import User
# Create your models here.
class Table(models.Model):
    User = models.OneToOneField(User, verbose_name=("linked_user"), on_delete=models.CASCADE)
    type_choices = (
        ('1', 'booked'),
        ('2', 'reserved'),
        ('3', 'free'),
    )
    name = models.CharField(max_length=50)
    choice_type = models.CharField(max_length=1, choices=type_choices)


class Type(models.Model):
    name = models.CharField(max_length=50)
    choice = models.BooleanField()


class Food(models.Model):
    name = models.CharField(max_length=50)
    pricePerQuantity = models.IntegerField()
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    rating = JSONField()
    orderCount = models.IntegerField()
    description = models.CharField(max_length=100)
    imageUrl = models.URLField()


class Customer(models.Model):
    mac_id = models.CharField(max_length=50)


class Orders(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    food = models.ManyToManyField(Food)
    quantity = ArrayField(models.IntegerField())
    dateOfCreation = models.DateTimeField()
    costOfThisOrder = ArrayField(models.IntegerField())
