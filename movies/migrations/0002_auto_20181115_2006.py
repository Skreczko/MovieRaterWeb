# Generated by Django 2.1.2 on 2018-11-15 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='duration',
            field=models.PositiveSmallIntegerField(help_text='in minutes'),
        ),
    ]
