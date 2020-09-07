from django.shortcuts import render, redirect
from .models import *
import json
# Create your views here.


def home (request):
    return render(request,'home.html')

def update(request):
    if request.user.is_superuser:
        with open('/Users/leejeongyeob/delicious/final_final_data.json') as json_file:
            json_data = json.load(json_file)
        for i in range(len(json_data)):
            restaurant = Restaurant()
            restaurant.name = json_data[i]['title']
            restaurant.link = json_data[i]['link']
            restaurant.mainfood = json_data[i]['main_food']
            restaurant.category = json_data[i]['category']
            restaurant.episode = json_data[i]['episode']
            restaurant.address = json_data[i]['address']
            restaurant.phoneNum = json_data[i]['phoneNum']
            restaurant.trivialInfo = json_data[i]['trivialInfo']
            restaurant.lat = json_data[i]['lat']
            restaurant.lng = json_data[i]['lng']
            restaurant.save()
            for j in json_data[i]['menus']:
                menulist = Menus()
                menulist.restaurant = restaurant
                menulist.menu = j
                menulist.save()


    return redirect(home)





    return redirect(home)