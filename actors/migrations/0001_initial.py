# Generated by Django 2.1.2 on 2018-11-24 20:54

import actors.models
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('movies', '__first__'),
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
                ('is_crew', models.BooleanField(choices=[(False, 'No'), (True, 'Yes')], default=False, verbose_name='Is crew member? (i.e. director, composer sountrack, costume designer)')),
            ],
            options={
                'ordering': ('last_name', 'name'),
            },
        ),
        migrations.CreateModel(
            name='ActorComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, max_length=1000, null=True)),
                ('stars', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
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
        migrations.CreateModel(
            name='ActorRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=100)),
                ('picture', models.ImageField(blank=True, null=True, upload_to=actors.models.ActorRole.upload_path)),
                ('actor', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='actor_role', to='actors.Actor')),
                ('movie', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='movie_role', to='movies.Movie')),
            ],
            options={
                'ordering': ('actor', 'movie'),
            },
        ),
        migrations.CreateModel(
            name='CrewRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('Director', 'Director'), ('Producer', 'Producer'), ('Set_Designer', 'Set Designer'), ('Costume_Designer', 'Costume Designer'), ('Prop_Master', 'Prop Master'), ('Makeup_Artist', 'Makeup Artist'), ('Movie_Editor', 'Movie Editor'), ('Other', 'Other')], max_length=100)),
                ('picture', models.ImageField(blank=True, null=True, upload_to=actors.models.CrewRole.upload_path)),
                ('actor', models.OneToOneField(limit_choices_to={'is_crew': True}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='actor_crew_role', to='actors.Actor')),
                ('movie', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='movie_crew_role', to='movies.Movie')),
            ],
            options={
                'ordering': ('role', 'actor', 'movie'),
            },
        ),
    ]
