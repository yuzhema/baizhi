from django.db import models

# Create your models here.

class Baizhi(models.Model):
    user=models.CharField(max_length=20,verbose_name='用户名')
    pwd=models.CharField(max_length=20,verbose_name='密码')
    usertel=models.CharField(max_length=20)
    email=models.CharField(max_length=20,verbose_name='邮箱')
    c_time = models.DateTimeField(auto_now_add=True)
    has_confirmed=models.BooleanField(default=False,verbose_name='是否确认')
    salt=models.CharField(max_length=20,verbose_name='yan')
    class Meta:
        db_table='t_baizhi'
        verbose_name='用户'
        verbose_name_plural='用户'

class ConfirmString(models.Model):
    code=models.CharField(max_length=256,verbose_name='注册码')
    user=models.OneToOneField('Baizhi',on_delete=models.CASCADE,verbose_name='关联的用户')
    c_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    class Meta:
        # ordering=['c_time']
        db_table = 'c_time'
        verbose_name='确认码'
        verbose_name_plural='确认码'

