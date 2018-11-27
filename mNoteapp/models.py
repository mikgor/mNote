from django.db import models
from django.contrib.auth.models import AbstractUser

class Note(models.Model):
    title = models.CharField('Tytuł', max_length=100)
    text = models.TextField('Treść')

class AppUser(AbstractUser):
    notes = models.ManyToManyField(Note)
    groups = models.ManyToManyField('Group')

    def __str__(self):
        return self.username

class Group(models.Model):
    name = models.CharField('Nazwa', max_length=100)
    owner = models.CharField('Właściciel', max_length=100)
    notes = models.ManyToManyField(Note)
    users = models.ManyToManyField(AppUser)

    def __str__(self):
        return self.name
