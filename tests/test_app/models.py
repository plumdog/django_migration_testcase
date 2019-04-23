from django.db import models


class MyModel(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField(null=True)
    double_number = models.IntegerField(null=True)


class ForeignModel(models.Model):
    name = models.CharField(max_length=100)
    my = models.ForeignKey(MyModel, on_delete=models.CASCADE)


class MySecondModel(models.Model):
    name = models.CharField(max_length=100, unique=True)
