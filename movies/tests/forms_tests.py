from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from movies.models import Movie, MovieCategory, MovieComment, MovieGallery
from accounts.models import MyUser
from movies.forms import MovieForm, MovieCategoryForm
import os
from django.utils.text import slugify
# Create your tests here.

class MovieFormTestCase(TestCase):
	def create_movie(self,
			title='Robin Hood',
			year_of_production=2018,
			production='US',
			budget=48027682,
			duration=104,
			description='Movie about Robin Hood.'
					 ):
		return Movie.objects.create(title=title,
									year_of_production=year_of_production,
									production=production,
									budget=budget,
									duration=duration,
									description=description
									)

	def test_movie_valid_form(self):
		movie = self.create_movie()
		data = {'title': movie.title,
				"year_of_production": movie.year_of_production,
				"production": movie.production,
				"budget": movie.budget,
				"duration": movie.duration,
				"description": movie.description}
		form = MovieForm(data=data)
		self.assertTrue(form.is_valid())
		self.assertEqual(form.cleaned_data.get('title'), movie.title)
		self.assertEqual(form.cleaned_data.get("year_of_production"), movie.year_of_production)
		self.assertEqual(form.cleaned_data.get("production"), movie.production)
		self.assertEqual(form.cleaned_data.get("budget"), movie.budget)
		self.assertEqual(form.cleaned_data.get("duration"), movie.duration)
		self.assertEqual(form.cleaned_data.get("description"), movie.description)

		self.assertNotEqual(form.cleaned_data.get('title'), 'Avatar')
		self.assertNotEqual(form.cleaned_data.get("year_of_production"), 2005)
		self.assertNotEqual(form.cleaned_data.get("production"), 'PL')
		self.assertNotEqual(form.cleaned_data.get("budget"), 1000)
		self.assertNotEqual(form.cleaned_data.get("duration"), 105)
		self.assertNotEqual(form.cleaned_data.get("description"), 'Some description about movie!')

	def test_movie_invalid_form(self):
		movie = self.create_movie()
		data = {'title': "",
				"year_of_production": movie.year_of_production,
				"production": movie.production,
				"budget": movie.budget,
				"duration": movie.duration,
				"description": movie.description}
		form = MovieForm(data=data)
		self.assertFalse(form.is_valid())
		self.assertNotEqual(form.cleaned_data.get('title'), movie.title)

class MovieCategoryFormTestCase(TestCase):
	def create_movie(self,
			title='Robin Hood',
			year_of_production=2018,
			production='US',
			budget=48027682,
			duration=104,
			description='Movie about Robin Hood.'
					 ):
		return Movie.objects.create(title=title,
									year_of_production=year_of_production,
									production=production,
									budget=budget,
									duration=duration,
									description=description
									)

	def test_form_valid(self):
		# movie = self.create_movie()
		# cat_action.related_movie.add(movie)
		# cat_fantasy.related_movie.add(movie)
		# cat_war.related_movie.add(movie)
		categories = ['Adventure', 'Animation', 'Anime']
		data = { 'category': ['Adventure', 'Animation', 'Anime', 'War'] }
		form = MovieCategoryForm(data=data)
		self.assertTrue(form.is_valid())
		self.assertEqual(form.cleaned_data.get('category'), 1)



#['Adventure', 'Animation', 'Anime']






