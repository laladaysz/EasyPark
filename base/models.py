from django.db import models

# Create your models here.

class plate_register(models.Model):
    number_plate = models.CharField(max_length=20)

class crop_spaces(models.Model):
    crop = models.ImageField(upload_to='images/')