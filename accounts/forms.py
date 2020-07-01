from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Order, Customer
from django.contrib.auth.forms import UserCreationForm
from django import forms


class CustomerFrom(ModelForm):
    class Meta:
        model = Customer
        field = '__all__'
        exclude = ['user']


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
