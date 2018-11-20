from django.db import models
from django.utils.text import slugify

from datetime import timedelta, datetime, date
from django.utils.timesince import timesince
from django.utils import timezone

from django.db.models.signals import pre_save
import os, random, string
from django.urls import reverse

from django_countries.fields import CountryField
from movies.models import Movie

# Create your models here.


class Actor(models.Model):

	def upload_path(instance, filename):
		extension = filename.split('.')[-1]
		filename = '{}.{}'.format(instance.slug,extension)
		return os.path.join(
			 'actors/',"%s" % instance.slug, filename)

	name = models.CharField(max_length=128, default="")
	slug = models.SlugField(unique=True)
	last_name = models.CharField(max_length=128,  default="")
	nationality = CountryField()
	city_of_birth = models.CharField(max_length=50)
	photo = models.ImageField(null=True, blank=True, upload_to=upload_path)
	biography = models.TextField(default="", blank=True)
	born = models.DateField()
	if_died = models.BooleanField(default=False, verbose_name="cross if dead")
	died = models.DateField(blank=True, null=True, default=None,)
	movies = models.ManyToManyField(Movie, related_name='related_actors')

	def __str__(self):
		return self.name + " " + self.last_name

	class Meta:
		ordering = ('last_name', 'name')


	@property
	def actor_age(self):
		if not self.if_died:
			age = timesince(self.born).split(',')[0]
			return '{} old'.format(age)
		elif self.died:
			age = int((self.died-self.born).days/365)
			return '{} years old'.format(age)
		else:
			return "Edit this section and choose the date of death"

	def average_stars(self):
		rates = ActorComment.objects.filter(actor=self)
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
		return reverse('actor_detail', kwargs={"slug":self.slug})


class ActorComment(models.Model):
	STARS = (
		(1, '1'),
		(2, '2'),
		(3, '3'),
		(4, '4'),
		(5, '5'),
		(6, '6'),
		(7, '7'),
		(8, '8'),
		(9, '9'),
		(10, '10'),
	)

	actor = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name="comments")
	comment = models.TextField(max_length=1000,blank=True, null=True)
	stars = models.IntegerField(choices=STARS)
	publish_date = models.DateTimeField(auto_now_add=True, auto_now=False)
	edited_date = models.DateTimeField(auto_now_add=False, auto_now=True)



	def __str__(self):
		return str(self.actor)

	def added_time(self):
		return '{t} ago'.format(t=timesince(self.publish_date))

	def edited_time(self):
		return '{t} ago'.format(t=timesince(self.edited_date))


class ActorGallery(models.Model):
	actor = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name="actor_gallery")

	def upload_path(instance, filename):
		extension = filename.split('.')[-1]
		random_name = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(9))
		filename='{}.{}'.format(random_name, extension)
		return os.path.join(
			 'actors/{}/gallery/{}'.format(instance.actor.slug, filename))
	picture = models.ImageField(upload_to=upload_path)

	def __str__(self):
		return str(self.actor)


class ActorRole(models.Model):
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie_role")
	actor = models.OneToOneField(Actor, on_delete=models.CASCADE, related_name="actor_role")
	role = models.CharField(max_length=100)
	def upload_path(instance, filename):
		extension = filename.split('.')[-1]
		random_name = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(9))
		filename='{}.{}'.format(random_name, extension)
		return os.path.join(
			 'movies/{m}/cast/{a} as {r}/{file}'.format(m=instance.movie.slug, a=instance.actor, r=instance.role, file=filename))
	picture = models.ImageField(null=True, blank=True, upload_to=upload_path)

	def __str__(self):
		return str("{movie} - {actor} - {role}".format(movie=self.movie, actor=self.actor, role=self.role))

	class Meta:
		ordering = ('actor','movie')


def slug_create(instance, new_slug=None):
	slug = slugify(str(instance.last_name + ' ' + instance.name))
	if new_slug is not None:
		slug = new_slug
	qs = Actor.objects.filter(slug=slug)
	if qs.exists():
		new_slug = "{}-{}".format(slug, qs.first().id)
		return slug_create(instance, new_slug=new_slug)
	return slug


def pre_save_actors(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slug_create(instance)


pre_save.connect(pre_save_actors, sender = Actor)

