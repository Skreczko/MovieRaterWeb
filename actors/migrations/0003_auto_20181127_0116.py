# Generated by Django 2.1.2 on 2018-11-27 00:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actors', '0002_auto_20181126_0138'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='actor',
            options={'ordering': ('-is_crew', 'last_name', 'name')},
        ),
    ]
