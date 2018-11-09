from django.db import models
from django.utils.text import slugify
from datetime import timedelta, datetime, date
from django.utils.timesince import timesince
from django.utils import timezone
from django.db.models.signals import pre_save

# Create your models here.


class Actor(models.Model):
	name = models.CharField(max_length=128, default="")
	slug = models.SlugField(unique=True)
	last_name = models.CharField(max_length=128,  default="")
	photo = models.ImageField(null=True, blank=True, upload_to='actors')
	biography = models.TextField(default="", blank=True)
	birth = models.DateField(blank=True, null=True,)

	def __str__(self):
		return self.name + " " + self.last_name



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
	actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
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




def slug_create(instance, new_slug=None):
	slug = slugify(str(instance.name + ' ' + instance.last_name))
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

