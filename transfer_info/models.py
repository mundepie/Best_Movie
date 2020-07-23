from django.db import models

# Employees table to contain all the employye information.

class Movies(models.Model):
    name = models.CharField(max_length=200, primary_key = True)
    start_day = models.IntegerField()
    start_month = models.CharField(max_length=3)
    end_day = models.IntegerField()
    end_month = models.CharField(max_length=3)
