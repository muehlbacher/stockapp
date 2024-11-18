from django.db import models

# Create your models here.
class Company:
    name = models.CharField(max_length=100)
    revenue = models.IntegerField()