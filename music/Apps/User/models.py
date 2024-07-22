from django.db import models
from django.contrib.auth.models import AbstractUser
# 引入内置信号
from django.db.models.signals import post_save
# 引入信号接收器的装饰器
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
class CustomUser(AbstractUser):
    class Meta:
        db_table = 'custom_user'

    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')
    nickname = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    def __str__(self):
        return '{}'.format(self.username)

class Profile(models.Model):
    class Meta:
        db_table = 'profile_model'
    # 级联删除，也就是当删除主表的数据时候从表中的数据也随着一起删除
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='Profile/avatars/%Y%m%d/', null=True, blank=True, default='Profile/default/avatar.png')
    info = models.TextField(null=True, blank=True, default='无', max_length=120)
    gender_choices = (
    (0, '无'),
    (1, '男'),
    (2, '女'),
)
    gender = models.SmallIntegerField(choices=gender_choices, default=0, blank=True, null=True)
    bod = models.DateField(null=True, blank=True)


    def __str__(self):
        return '{}'.format(self.user.username)

"""在 User 模型的实例保存后自动管理与其关联的 Profile 实例，确保它们保持同步和一致。"""
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()




    

    
