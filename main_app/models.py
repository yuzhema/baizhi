from django.db import models

# Create your models here.

class Projects(models.Model):
    title=models.CharField(max_length=200)
    salary=models.CharField(max_length=200)
    academics=models.CharField(max_length=200)
    experience=models.CharField(max_length=200)
    company=models.CharField(max_length=200)
    city=models.CharField(max_length=200)
    describes=models.CharField(max_length=2000)

    class Meta:
        db_table='t_projects'

