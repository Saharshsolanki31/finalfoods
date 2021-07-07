from django.shortcuts import render

#function For Home
from restaurant.models import restaurant


def index(request):
    rest_data = restaurant.objects.all()
    return  render(request,'index.html',{'restaurant_data':rest_data})