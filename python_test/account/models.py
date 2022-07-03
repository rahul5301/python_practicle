from dataclasses import fields
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User ,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20)
    otp = models.CharField(max_length=6)
    
class Category(models.Model):
    title = models.CharField(max_length=255)
    class Meta:
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.title
class Book(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=100, default='Rahul Darji')
    isbn = models.CharField(max_length=13)
    price = models.IntegerField()
    quantity = models.IntegerField()
    description = models.TextField()
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.title