from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User
from django.db.models.expressions import F
from django.db.models.fields import EmailField
import uuid
from django.shortcuts import render
from django.utils.text import slugify
from django.db.models.signals import post_save, post_delete

class User(AbstractUser):
    is_manager = models.BooleanField(default=False)
    is_developer = models.BooleanField(default=False)

# # Create your models here.
class PMProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.user.username

class DevProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.user.username
    

class Ticket(models.Model):
    user = models.ForeignKey(PMProfile, on_delete=models.CASCADE, null=True)
    accessed_by = models.ForeignKey(DevProfile, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    OPEN = 'Open'
    ACCEPTED = 'Accepted'
    COMPLETED = 'Completed'
    CLOSED = 'Clossed'
    TICKET_STATUS = (
        ('Open', 'Open'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Closed', 'Closed'), 
    )
    status = models.CharField(max_length=200, choices=TICKET_STATUS, default=OPEN)
    slug = models.SlugField(default="", null=False)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    # def get_absolute_url(self):
    #     return reverse("opentickets")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.status)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

