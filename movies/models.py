from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.validators import MaxValueValidator
from django.utils.timesince import timesince
from django.db.models.signals import pre_save
import os, random, string
from django.urls import reverse
from django_countries.fields import CountryField
from django.utils.translation import ugettext_lazy as _


YEARS = ((x, x) for x in range(1930, 2041))
DURATION = ((x, x) for x in range(0, 721))
CATEGORIES = (
	('Action', 'Action'),
	('Adventure', 'Adventure'),
	('Animation', 'Animation'),
	('Anime', 'Anime'),
	('Biography', 'Biography'),
	('Comedy', 'Comedy'),
	('Crime', 'Crime'),
	('Documentary', 'Documentary'),
	('Drama', 'Drama'),
	('Family', 'Family'),
	('Fantasy', 'Fantasy'),
	('Film - Noir', 'Film-Noir'),
	('History', 'History'),
	('Horror', 'Horror'),
	('Musical', 'Musical'),
	('Romence', 'Romence'),
	('Sci-Fi', 'Sci-Fi'),
	('Thriller', 'Thriller'),
	('War', 'War'),
	('Western', 'Western'),
)
STARS = (
		(1, '1'),
		(2, '2'),
		(3, '3'),
		(4, '4'),
		(5, '5'),
	)
# Create your models here.


class Movie(models.Model):

	def upload_path(instance, filename):
		extension = filename.split(".")[-1]
		filename = "{}.{}".format(instance.slug, extension)
		return os.path.join(
			'movies/', "%s" % instance.slug, filename)

	title = models.CharField(max_length=50)
	slug = models.SlugField(unique=True)
	year_of_production = models.PositiveSmallIntegerField()
	production = CountryField()
	budget = models.PositiveIntegerField(help_text="in dollars", validators=[MaxValueValidator(500000000,"The maximum value is 500 million ")])
	poster = models.ImageField(null=True, blank=True, upload_to=upload_path)
	duration = models.PositiveSmallIntegerField(help_text="in minutes")
	description = models.CharField(max_length=295, default="", null=True,blank=True, help_text="295 character maximum.")

	class Meta:
		ordering = ('title',)



	def __str__(self):
		return str(self.title) + " ({})".format(str(self.year_of_production))

	@property
	def average_stars(self):
		rates = MovieComment.objects.filter(movie=self)
		rates_amount = len(rates)
		rating = 0
		for item in rates:
			rating += item.stars
		if rating == 0:
			rating = 0
			return rating,rates_amount
		else:
			rating = float("{0:.2f}".format(rating/rates_amount))
			return rating, rates_amount

	def get_to_detail(self):
		return reverse('movie_detail', kwargs={"slug": self.slug})

class MovieCategory(models.Model):

	related_movie = models.ManyToManyField(Movie,related_name='movie_category')
	category = models.CharField(max_length=100, choices=CATEGORIES)

	def __str__(self):
		return str(self.category)


class MovieComment(models.Model):
	added_by = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie_comments")
	comment = models.CharField(max_length=2000, blank=True, null=True, )
	stars = models.IntegerField(choices=STARS)
	publish_date = models.DateTimeField(auto_now_add=True, auto_now=False)
	edited_date = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __str__(self):
		return str(self.movie)

	def added_time(self):
		return '{t} ago'.format(t=timesince(self.publish_date))

	def edited_time(self):
		return '{t} ago'.format(t=timesince(self.edited_date))




class MovieGallery(models.Model):
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie_gallery")

	def upload_path(instance, filename):
		extension = filename.split('.')[-1]
		random_name = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(9))
		filename='{}.{}'.format(random_name, extension)
		return os.path.join(
			 'movies/{}/gallery/{}'.format(instance.movie.slug, filename))
	picture = models.ImageField(upload_to=upload_path)

	def __str__(self):
		return str(self.movie)

def slug_create(instance, new_slug=None):
	slug = slugify(str(instance.title))
	if new_slug is not None:
		slug = new_slug
	qs = Movie.objects.filter(slug=slug)
	if qs.exists():
		new_slug = "{}-{}".format(slug, qs.first().id)
		return slug_create(instance, new_slug=new_slug)
	return slug

def pre_save_movies(instance, sender, *args, **kwargs):
	if not instance.slug:
		instance.slug = slug_create(instance)

pre_save.connect(pre_save_movies, sender=Movie)