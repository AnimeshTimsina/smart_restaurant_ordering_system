from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save





# Create your models here.
class Table(models.Model):
    User = models.OneToOneField(User, verbose_name=("linked_user"), on_delete=models.CASCADE)
    type_choices = (
        ('1', 'booked'),
        ('2', 'reserved'),
        ('3', 'free'),
    )
    name = models.CharField(max_length=50, blank = True, null = True)
    choice_type = models.CharField(max_length=1, choices=type_choices)

    def __str__(self):
        return self.name

@receiver(post_save, sender=Table)
def _post_save_receiver(sender,instance,created, **kwargs):
    if created:
        instance.name = instance.User.username
        instance.save()
    


class Type(models.Model):
    name = models.CharField(max_length=50)
    choice = models.BooleanField()

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(max_length=50)
    pricePerQuantity = models.IntegerField()
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    rating = JSONField(null=True,blank=True)
    orderCount = models.IntegerField(default=0)
    description = models.CharField(max_length=100)
    imageUrl = models.URLField(null=True,blank=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    mac_id = models.CharField(max_length=50)


class Orders(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    food = models.ManyToManyField(Food)
    quantity = ArrayField(models.IntegerField())
    dateOfCreation = models.DateTimeField()
    costList = ArrayField(models.IntegerField(),blank=True,null=True)
    totalCost = models.IntegerField(default=0)
    arrived = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return str(self.table)

