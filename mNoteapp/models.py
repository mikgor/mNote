from django.db import models
from django.contrib.auth.models import AbstractUser

class Note(models.Model):
    title = models.CharField('Tytuł', max_length=100)
    text = models.TextField('Treść')

class AppUser(AbstractUser):
    notes = models.ManyToManyField(Note)

    def __str__(self):
        return self.email
