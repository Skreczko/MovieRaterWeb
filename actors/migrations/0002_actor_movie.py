# Generated by Django 2.1.2 on 2018-11-19 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0010_auto_20181118_1539'),
        ('actors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='actor',
            name='movie',
            field=models.ManyToManyField(to='movies.Movie'),
        ),
    ]
