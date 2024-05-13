from django.db.models import fields
from django.db.models.enums import Choices
import django_filters
from django_filters import DateFilter, CharFilter
from .models import *

class EmployeeFilter(django_filters.FilterSet):
    # city = CharFilter(field_name='city', lookup_expr='icontains')
    class Meta:
        model = Employee
        fields = '__all__'
        exclude = ['user','job','name','experience','amountperhour','contact','adharno','address','zipcode', 'emp_rating', 'job_count', 'rating_count','image']