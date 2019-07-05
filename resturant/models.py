from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.contrib.auth.models import ( BaseUserManager, AbstractBaseUser )
from django.core.validators import RegexValidator

USERNAME_REGEX = '^[a-zA-Z0-9,+-]*$'

class MyUserManager(BaseUserManager):
	def create_user(self, username, email, password=None):
		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(
					username = username,
					email = self.normalize_email(email)
				)
		user.set_password(password)
		user.save(using=self._db)
		return user
		# user.password = password # bad - do not do this

	def create_superuser(self, username, email, password=None):
		user = self.create_user(
				username, email, password=password
			)
		user.is_admin = True
		user.is_staff = True
		user.save(using=self._db)
		return user



class MyUser(AbstractBaseUser):
	username = models.CharField(
					max_length=300,
					validators = [
						RegexValidator(regex = USERNAME_REGEX,
										message='Username must be alphanumeric or contain numbers',
										code='invalid_username'
							)],
					unique=True
				)
	email = models.EmailField(
			max_length=255,
			unique=True,
			verbose_name='email address'
		)
	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)

	objects = MyUserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	def __str__(self):
		return self.email

	def get_short_name(self):
		# The user is identified by their email address
		return self.email


	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True


# Create your models here.
class Table(models.Model):
    type_choices = (
        ('1','booked'),
        ('2','reserved'),
        ('3','free'),
    )
    name=models.CharField(max_length=50)
    choice_type = models.CharField(max_length=1,choices = type_choices)

class Type(models.Model):
    name=models.CharField(max_length=50)
    choice=models.BooleanField()

class Food(models.Model):
    name=models.CharField(max_length=50)
    pricePerQuantity=models.IntegerField()
    type=models.ForeignKey(Type,on_delete=models.CASCADE)
    rating=JSONField()
    orderCount=models.IntegerField()
    description=models.CharField(max_length=100)
    imageUrl=models.URLField()

class Customer(models.Model):
    mac_id=models.CharField(max_length=50)


class Orders(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    table=models.ForeignKey(Table,on_delete=models.CASCADE)
    food=models.ManyToManyField(Food)
    quantity=ArrayField(models.IntegerField())
    dateOfCreation=models.DateTimeField()
    costOfThisOrder=ArrayField(models.IntegerField())
