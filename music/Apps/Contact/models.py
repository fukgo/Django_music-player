from django.db import models


class ContactModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='姓名')
    email_or_phone = models.CharField(max_length=100, verbose_name='联系方式(邮箱或电话)')
    message = models.TextField(verbose_name='留言')
