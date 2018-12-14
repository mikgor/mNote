from django.db import models
from django.contrib.auth.models import AbstractUser

class Note(models.Model):
    TYPE_CHOICES = (
    ("text", "Tekst"),
    ("todo", "To-do"),
    ("list", "Lista"),
    )
    type = models.CharField('Typ', max_length=5, choices=TYPE_CHOICES, default="text")
    title = models.CharField('Tytuł', max_length=100)
    text = models.TextField('Treść')
    groupId = models.IntegerField(default=0) #0 = private
    color = models.CharField('Kolor', max_length=14, default="dodgerblue")

    def save(self, *args, **kwargs):
        if not self.groupId == 0 and not self.pk is None:
            g = Group.objects.get(id=self.groupId)
            notification = 'Notatka {0} grupy {1} została zmodyfikowana'.format(self.title, g.name)
            for user in g.users.all():
                user.NewNotification(text=notification)
        super(Note, self).save(*args, **kwargs)

class Notification(models.Model):
    text = models.TextField('Treść')
    read = models.BooleanField(default=False)

class AppUser(AbstractUser):
    notes = models.ManyToManyField(Note)
    groups = models.ManyToManyField('Group')
    notifications = models.ManyToManyField(Notification)

    def __str__(self):
        return self.username

    def NewNotification(self, text):
        n = Notification.objects.create()
        n.text = text
        n.save()
        self.notifications.add(n)

class Group(models.Model):
    name = models.CharField('Nazwa', max_length=100)
    owner = models.CharField('Właściciel', max_length=100)
    notes = models.ManyToManyField(Note)
    users = models.ManyToManyField(AppUser, verbose_name="Użytkownicy")

    def __str__(self):
        return self.name
