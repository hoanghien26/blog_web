from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,AbstractUser
# Create your models here.
class CustomUser(AbstractUser):
    phone_number=models.CharField(max_length=15, blank=True)
    avatar=models.ImageField(upload_to='avatars/', null=True, blank=True)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='Các nhóm mà người dùng này thuộc về...',
        related_name="customuser_set",  # Thêm dòng này
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='quyền người dùng',
        blank=True,
        help_text='Các quyền cụ thể cho người dùng này...',
        related_name="customuser_set",  # Thêm dòng này
        related_query_name="user",
    )