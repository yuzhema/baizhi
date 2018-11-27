from django.db import models

# Create your models here.

class Baizhi(models.Model):
    user=models.CharField(max_length=20)
    pwd=models.CharField(max_length=20)
    usertel=models.CharField(max_length=20)
    email=models.CharField(max_length=20)
    class Meta:
        db_table='t_baizhi'


