from django.db import models
from django.utils.text import slugify

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
	comment = models.TextField(max_length=1000)
	stars = models.IntegerField(choices=STARS)

	def __str__(self):
		return str(self.actor)







