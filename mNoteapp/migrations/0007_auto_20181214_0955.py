# Generated by Django 2.0.7 on 2018-12-14 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mNoteapp', '0006_auto_20181211_2150'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Treść')),
                ('read', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='appuser',
            name='notifications',
            field=models.ManyToManyField(to='mNoteapp.Notification'),
        ),
    ]
