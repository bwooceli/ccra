from tkinter import CASCADE
from django.db import models

# Create your models here.
class Car(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.CharField(max_length=255)

    auto_admin_reg = True

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=255)
    auto_admin_reg = True

    def __str__(self):
        return self.title


class Division(models.Model):
    title = models.CharField(max_length=255)
    auto_admin_reg = True

    def __str__(self):
        return self.title


class CarEventRegistration(models.Model):
    car = models.ForeignKey("Car", on_delete=models.CASCADE)
    event = models.ForeignKey("Event", on_delete=models.CASCADE)
    division = models.ForeignKey("Division", on_delete=models.CASCADE)
    registration_id = models.CharField(max_length=15)

    auto_admin_reg = True
    

class HeatResult(models.Model):
    event = models.ForeignKey("Event", on_delete=CASCADE)
    heat_number = models.IntegerField()
    lane_number = models.IntegerField()
    car = models.ForeignKey("Car")
    result = models.FloatField()
    
