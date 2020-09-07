from django.db import models

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length = 75, null=True)
    link = models.CharField(max_length = 200, null=True)
    mainfood = models.CharField(max_length = 50, null=True)
    episode = models.CharField(max_length = 25, null=True)
    mainfood = models.CharField(max_length = 50, null=True)
    address = models.CharField(max_length = 100, null=True)
    phoneNum = models.CharField(max_length = 30, null=True)
    trivialInfo = models.TextField(null=True)
    lat = models.CharField(max_length = 50, null=True)
    lng = models.CharField(max_length = 50, null=True)

class Menus(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete = models.CASCADE)
    menu = models.CharField(max_length = 250)