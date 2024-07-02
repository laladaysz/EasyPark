from django.db import models

# Create your models here.

class owner(models.Model):
    area =  models.CharField(max_length=100)
    number_plate = models.CharField(max_length=20)

# class crop_spaces(models.Model):
#     crop = models.ImageField(upload_to='images/')

