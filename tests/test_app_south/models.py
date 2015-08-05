from django.db import models

# Create your models here.

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField(null=True)
    double_number = models.IntegerField(null=True)
