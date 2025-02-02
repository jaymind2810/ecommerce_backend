from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager
from datetime import datetime


class User(AbstractUser):

    ROLE_CHOICES = [
        ('User', 'User'),
        ('Management', 'Management'),
        ('Admin', 'Admin'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='User')
    mobile = models.CharField(max_length=20, blank=True, default='0')
    personal_address = models.TextField(max_length=200, blank=True, default='-')
    city = models.CharField(max_length=20, blank=True, default='-')
    user_photo = models.ImageField(upload_to='users/', blank=True, default='users/avatar-3.jpg')
    user_stripe_id = models.CharField(max_length=20, blank=True, null=True)
    is_delete = models.BooleanField(max_length=20, default=False)

    def save(self, *args, **kwargs):
        print(self.is_superuser, "----------iiiiiii--", self.is_staff)
        if self.is_superuser:
            self.role = 'Admin'
            # masteruser = Group.objects.get(name="masteruser")
            # print(masteruser, "-------masteruser----------")
            # self.groups.add(masteruser)
        if self.is_staff and self.is_superuser is not True:
            self.role = 'Management'
        super().save(*args, **kwargs)


class Main(models.Model):

    name = models.CharField(default="My Site", max_length=128)
    about = models.TextField(default="-")
    tell = models.CharField(default="+91 ", max_length=255)
    link = models.CharField(default="-", max_length=255)
    email = models.CharField(default="-", max_length=255)
    location = models.CharField(default="Ahmedabad, India", max_length=255)

    fb = models.CharField(default="fb", max_length=128)
    tw = models.CharField(default="tw", max_length=128)
    google = models.CharField(default="gg", max_length=128)
    pt = models.CharField(default="pt", max_length=128)

    picname = models.TextField(default="-")
    picurl = models.TextField(default="-")

    set_name = models.CharField(default="Site Settings", max_length=128)

    is_delete = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True, editable=False, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, editable=False, blank=True, null=True)

    def __str__(self):
        return self.set_name + " | "+ str(self.pk)

