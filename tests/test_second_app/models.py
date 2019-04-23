from django.db import models


class MyModel(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField(null=True)
    my_model = models.ForeignKey(
        'test_app.MyModel', blank=True, null=True, on_delete=models.CASCADE)
