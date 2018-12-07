from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.timesince import timesince
from django.db.models.signals import pre_save
import os, random, string
from django.urls import reverse
from django_countries.fields import CountryField
from movies.models import Movie
from datetime import datetime
# Create your models here.

YEARS = [x for x in range(1930, 2041)]
YES_NO = (
	(False, 'No'),
	(True, 'Yes')
)

STARS = (
	(1, '1'),
	(2, '2'),
	(3, '3'),
	(4, '4'),
	(5, '5'),
)

CREW_ROLE = (
	('Director', 'Director'),
	('Producer', 'Producer'),
	('Set Designer', 'Set Designer'),
	('Costume Designer', 'Costume Designer'),
	('Prop Master', 'Prop Master'),
	('Makeup Artist', 'Makeup Artist'),
	('Movie Editor', 'Movie Editor'),
	('Other', 'Other'),

)


class Actor(models.Model):

	def upload_path(instance, filename):
		extension = filename.split('.')[-1]
		filename = '{}.{}'.format(instance.slug,extension)
		return os.path.join(
			 'actors/',"%s" % instance.slug, filename)

	name = models.CharField(max_length=128, default="")
	slug = models.SlugField(unique=True)
	last_name = models.CharField(max_length=128,  default="")
	original_name = models.CharField(max_length=128, null=True, blank=True)
	nationality = CountryField()
	city_of_birth = models.CharField(max_length=50)
	photo = models.ImageField(null=True, blank=True, upload_to=upload_path)
	biography = models.TextField(default="", blank=True)
	born = models.DateField()
	if_died = models.BooleanField(default=False, verbose_name="cross if dead")
	died = models.DateField(blank=True, null=True, default=None,)
	is_crew = models.BooleanField(default=False, choices=YES_NO, verbose_name='Is also crew member? (i.e. director, composer sountrack, costume designer)')


	def __str__(self):
		return self.name + " " + self.last_name

	class Meta:
		ordering = ('last_name', 'name')


	@property
	def actor_age(self):
		if not self.if_died:
			#age = timesince(self.born).split(',')[0]
			age = int(datetime.now().year- self.born.year)
			return age
		elif self.died:
			age = int((self.died-self.born).days/365)
			return age
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
		return reverse('actor_detail', kwargs={"slug": self.slug})

	def get_api_url(self):
		return reverse("actors-api:detail", kwargs={"slug": self.slug})


class ActorComment(models.Model):

	added_by = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
	actor = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name="actor_comments")
	comment = models.CharField(max_length=2000, blank=True, null=True, )
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
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie_role", null=True)
	actor = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name="actor_role", null=True)
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


class CrewRole(models.Model):
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie_crew_role", null=True)
	actor = models.OneToOneField(Actor, on_delete=models.CASCADE, related_name="actor_crew_role", null=True,
								 limit_choices_to={'is_crew': True})
	role = models.CharField(max_length=100, choices=CREW_ROLE)
	def upload_path(instance, filename):
		extension = filename.split('.')[-1]
		random_name = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(9))
		filename='{}.{}'.format(random_name, extension)
		return os.path.join(
			 'movies/{m}/crew/{a} as {r}/{file}'.format(m=instance.movie.slug, a=instance.actor, r=instance.role, file=filename))
	picture = models.ImageField(null=True, blank=True, upload_to=upload_path)

	def __str__(self):
		return str("{movie} - {actor} - {role}".format(movie=self.movie, actor=self.actor, role=self.role))

	class Meta:
		ordering = ('role', 'actor', 'movie')


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



#https://stackoverflow.com/questions/41783318/how-to-have-extra-django-model-fields-depending-on-the-value-of-a-field
# class ActorRole(models.Model):
# 	movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie_role", null=True)
# 	actor = models.OneToOneField(Actor, on_delete=models.CASCADE, related_name="actor_role", null=True)
# 	role = models.OneToOneField()
# 	def upload_path(instance, filename):
# 		extension = filename.split('.')[-1]
# 		random_name = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(9))
# 		filename='{}.{}'.format(random_name, extension)
# 		return os.path.join(
# 			 'movies/{m}/cast/{a} as {r}/{file}'.format(m=instance.movie.slug, a=instance.actor, r=instance.role, file=filename))
# 	picture = models.ImageField(null=True, blank=True, upload_to=upload_path)
#
# 	def __str__(self):
# 		return str("{movie} - {actor} - {role}".format(movie=self.movie, actor=self.actor, role=self.role))
#
# 	class Meta:
# 		ordering = ('actor','movie')
#
#
#
#
# class Cast(models.Model):
# 	role = models.CharField(max_length=100, choices=CREW_ROLE)
# 	class Meta:
# 		abstract = True
#
#
# class Crew(models.Model):
# 	role = models.CharField(max_length=100)
#
# 	class Meta:
# 		abstract = True

