# Generated by Django 2.1.2 on 2018-11-15 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_auto_20181115_2352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='description',
            field=models.CharField(blank=True, default='', help_text='295 character maximum.', max_length=295, null=True),
        ),
        migrations.AlterField(
            model_name='moviecomment',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
