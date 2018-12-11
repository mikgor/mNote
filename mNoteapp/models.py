from django.db import models
from django.contrib.auth.models import AbstractUser

class Note(models.Model):
    TYPE_CHOICES = (
    ("text", "Tekst"),
    ("todo", "To-do"),
    ("list", "Lista"),
    )
    type = models.CharField('Typ', max_length=5,  choices=TYPE_CHOICES, default="text")
    title = models.CharField('Tytuł', max_length=100)
    text = models.TextField('Treść')
    color = models.CharField('Kolor', max_length=14, default="dodgerblue")

class AppUser(AbstractUser):
    notes = models.ManyToManyField(Note)
    groups = models.ManyToManyField('Group')

    def __str__(self):
        return self.username

class Group(models.Model):
    name = models.CharField('Nazwa', max_length=100)
    owner = models.CharField('Właściciel', max_length=100)
    notes = models.ManyToManyField(Note)
    users = models.ManyToManyField(AppUser, verbose_name="Użytkownicy")

    def __str__(self):
        return self.name
