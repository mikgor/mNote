# Generated by Django 2.0.7 on 2018-12-11 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mNoteapp', '0003_note_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='color',
            field=models.CharField(default='dodgerblue', max_length=14, verbose_name='Kolor'),
        ),
    ]
