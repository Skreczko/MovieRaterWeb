# Generated by Django 2.1.2 on 2018-11-14 15:57

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import movies.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
                ('year_of_production', models.PositiveSmallIntegerField()),
                ('production', django_countries.fields.CountryField(max_length=2)),
                ('budget', models.PositiveIntegerField(help_text='in dollars')),
                ('poster', models.ImageField(blank=True, null=True, upload_to=movies.models.Movie.upload_path)),
                ('duration', models.PositiveSmallIntegerField()),
                ('description', models.TextField(blank=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='MovieCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Action', 'Action'), ('Adventure', 'Adventure'), ('Animation', 'Animation'), ('Anime', 'Anime'), ('Biography', 'Biography'), ('Comedy', 'Comedy'), ('Crime', 'Crime'), ('Documentary', 'Documentary'), ('Drama', 'Drama'), ('Family', 'Family'), ('Fantasy', 'Fantasy'), ('Film - Noir', 'Film-Noir'), ('History', 'History'), ('Horror', 'Horror'), ('Musical', 'Musical'), ('Romence', 'Romence'), ('Sci-Fi', 'Sci-Fi'), ('Thriller', 'Thriller'), ('War', 'War'), ('Western', 'Western')], max_length=100)),
                ('related_movie', models.ManyToManyField(to='movies.Movie')),
            ],
        ),
        migrations.CreateModel(
            name='MovieComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, max_length=1000, null=True)),
                ('stars', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')])),
                ('publish_date', models.DateTimeField(auto_now_add=True)),
                ('edited_date', models.DateTimeField(auto_now=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movie_comments', to='movies.Movie')),
            ],
        ),
        migrations.CreateModel(
            name='MovieGallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to=movies.models.MovieGallery.upload_path)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movie_gallery', to='movies.Movie')),
            ],
        ),
    ]
