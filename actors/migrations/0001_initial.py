# Generated by Django 2.1.2 on 2018-11-14 15:01

import actors.models
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=128)),
                ('slug', models.SlugField(unique=True)),
                ('last_name', models.CharField(default='', max_length=128)),
                ('nationality', django_countries.fields.CountryField(max_length=2)),
                ('city_of_birth', models.CharField(max_length=50)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=actors.models.Actor.upload_path)),
                ('biography', models.TextField(blank=True, default='')),
                ('born', models.DateField()),
                ('if_died', models.BooleanField(default=False, verbose_name='cross if dead')),
                ('died', models.DateField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ActorComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, max_length=1000, null=True)),
                ('stars', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')])),
                ('publish_date', models.DateTimeField(auto_now_add=True)),
                ('edited_date', models.DateTimeField(auto_now=True)),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='actors.Actor')),
            ],
        ),
        migrations.CreateModel(
            name='ActorGallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to=actors.models.ActorGallery.upload_path)),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actor_gallery', to='actors.Actor')),
            ],
        ),
    ]
