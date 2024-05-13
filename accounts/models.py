from django.core import validators
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

# Create your models here.

CITY_CHOICES = (
        ('', 'CITY'),
        ('TVM', 'TVM'),
        ('CALICUT', 'CALICUT'),
        ('KOCHIN', 'KOCHIN')
    )

class NewUser(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'customer'),
        (2, 'employee'),
        (3, 'admin'),
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, null=True, blank=True)


class JobList(models.Model):
    job = models.CharField(max_length=50)
    image = models.ImageField(upload_to = 'Jobs/', blank =True, null=True)

    def __str__(self):
        return self.job


class Customer(models.Model):
    users = models.OneToOneField(NewUser, on_delete=models.CASCADE, null= True)
    name = models.CharField(max_length=34, null=True, blank=True)
    contact = models.CharField(max_length=11, null=True, blank=True, validators=[RegexValidator(r'^\d{1,10}$')])
    adharno = models.CharField(
        max_length=12,
        null=True,
        blank=True,
        validators=[RegexValidator(r'^\d{12}$', message='Aadhar number must be a 12-digit number')]
    )
    address = models.CharField(max_length=34, null=True, blank=True)
    zipcode = models.CharField(max_length=6, null=True, blank=True, validators=[RegexValidator(r'^\d{1,10}$')])
    city = models.CharField(max_length=200, null=True, choices=CITY_CHOICES)
    
    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(NewUser, on_delete=models.CASCADE, null= True)
    name=models.CharField(max_length=34,null=True,blank=True)
    job = models.ForeignKey('JobList', on_delete=models.SET_NULL, null=True)
    experience = models.CharField(max_length=34, null=True, blank=True)
    amountperhour = models.CharField(max_length=34, null=True, blank=True)
    contact = models.CharField(max_length=11, null=True, blank=True, validators=[RegexValidator(r'^\d{1,10}$')])
    adharno = models.CharField(
        max_length=12,
        null=True,
        blank=True,
        validators=[RegexValidator(r'^\d{12}$', message='Aadhar number must be a 12-digit number')]
    )
    address = models.CharField(max_length=200, null=True, blank=True)
    zipcode = models.CharField(max_length=6, null=True, blank=True, validators=[RegexValidator(r'^\d{1,10}$')])
    city = models.CharField(max_length=34, null=True, choices=CITY_CHOICES)
    emp_rating = models.FloatField(max_length=3, null=True, blank=True)
    job_count = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='employee_images/', null=True, blank=True)

    def __str__(self):
        return self.name


class WorkDetails(models.Model):
    RATINGS = (
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5),
    )
    JOB_STATUS = (
        ('Unapproved','Unapproved'),
        ('Approved','Approved'),
        ('Closed','Closed')
    )

    customer_id = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True)
    employee_id = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=34, null=True, blank=True)
    job_status = models.CharField(max_length=34, null=True, blank=True, choices=JOB_STATUS)
    rating = models.IntegerField(null=True, blank=True, choices=RATINGS)

    def __str__(self):
        return self.location

