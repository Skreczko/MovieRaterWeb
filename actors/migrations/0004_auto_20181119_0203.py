# Generated by Django 2.1.2 on 2018-11-19 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actors', '0003_auto_20181119_0149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='movies',
            field=models.ManyToManyField(related_name='related_actors', to='movies.Movie'),
        ),
    ]