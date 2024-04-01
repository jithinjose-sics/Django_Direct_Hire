from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import fields
from .models import *

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = NewUser
#         fields = ['id', 'username', 'email', 'password']
#         exclude = ['user_type']

class UserForm(UserCreationForm):
    class Meta:
        model = NewUser
        fields = ['id', 'username', 'email', 'password1', 'password2']
        exclude = ['user_type']


class EmployeeForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'autocomplete': 'off', 'placeholder': 'Name', 'class': 'form-control', 'id': 'search-bar', 'required': ''}
    ))
    experience = forms.CharField(widget=forms.TextInput(
        attrs={'autocomplete': 'off', 'placeholder': 'Year Of Experience', 'class': 'form-control', 'id': 'search-bar',
               'required': ''}))
    job = forms.ModelChoiceField(label="", queryset=JobList.objects.all(), empty_label="Jobs")

    amountperhour = forms.CharField(widget=forms.TextInput(
        attrs={'autocomplete': 'off', 'placeholder': 'Amount Per Hour', 'class': 'form-control', 'id': 'search-bar',
               'required': ''}))
    contact = forms.CharField(widget=forms.TextInput(
        attrs={'autocomplete': 'off',  'placeholder': 'Mobile Number', 'class': 'form-control',
               'id': 'search-bar', 'required': ''}))
    adharno = forms.CharField(widget=forms.TextInput(
        attrs={'autocomplete': 'off', 'placeholder': 'Aadhar Number ', 'class': 'form-control', 'id': 'search-bar',
               'required': ''}))

    address = forms.CharField(widget=forms.TextInput(
        attrs={'autocomplete': 'off', 'placeholder': 'Address', 'class': 'form-control', 'id': 'search-bar',
               'required': ''}))
    zipcode = forms.CharField(widget=forms.TextInput(
        attrs={'autocomplete': 'off', 'placeholder': 'ZIP ', 'class': 'form-control', 'id': 'search-bar',
               'required': ''}))
    city = forms.ChoiceField(choices=CITY_CHOICES, required=False)

    class Meta:
        model = Employee
        fields = '__all__'
        exclude = ['user', ]


class CustomerForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(
        attrs={'autocomplete': 'off', 'placeholder': 'Name', 'class': 'form-control', 'id': 'search-bar',
               'required': ''}))

    contact = forms.CharField(widget=forms.TextInput(
        attrs={'autocomplete': 'off',  'placeholder': 'Mobile Number', 'class': 'form-control',
               'id': 'search-bar', 'required': ''}))
    adharno = forms.CharField(widget=forms.TextInput(
        attrs={'autocomplete': 'off', 'placeholder': 'Aadhar Number ', 'class': 'form-control', 'id': 'search-bar',
               'required': ''}))

    address = forms.CharField(widget=forms.TextInput(
        attrs={'autocomplete': 'off', 'placeholder': 'Address', 'class': 'form-control', 'id': 'search-bar',
               'required': ''}))
    zipcode = forms.CharField(widget=forms.TextInput(
        attrs={'autocomplete': 'off', 'placeholder': 'ZIP ', 'class': 'form-control', 'id': 'search-bar',
               'required': ''}))

    city = forms.ChoiceField(choices=CITY_CHOICES, required=False)


    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['users', ]