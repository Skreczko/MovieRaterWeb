from django.test import TestCase
from movies.models import Movie, MovieCategory, MovieComment
from movies.forms import MovieForm, MovieCategoryForm, MovieCommentForm
# Create your tests here.

class MovieTestCase(TestCase):
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

	def test_movie_comment_valid_form(self):
		movie = self.create_movie()
		movcom = MovieComment.objects.create(movie=movie, comment='Comment for Robin Hood', stars=3)
		data = {'comment': movcom.comment,
				"stars": movcom.stars, }
		form = MovieCommentForm(data=data)
		self.assertTrue(form.is_valid())
		self.assertEqual(form.cleaned_data.get('comment'), movcom.comment)
		self.assertEqual(form.cleaned_data.get("stars"), movcom.stars)

		self.assertNotEqual(form.cleaned_data.get('comment'), 'Some random comment')
		self.assertNotEqual(form.cleaned_data.get("stars"), 5)

	def test_movie_comment_invalid_form(self):
		movie = self.create_movie()
		movcom = MovieComment.objects.create(movie=movie, comment='Comment for Robin Hood', stars=3)
		data = {'comment': movcom.comment,
				"stars": 6}
		form = MovieCommentForm(data=data)
		self.assertFalse(form.is_valid())


class MovieCategoryFormTestCase(TestCase):
	def test_form_valid(self):
		data = { 'category': ['Adventure', 'Animation', 'Anime'] }
		form = MovieCategoryForm(data=data)
		self.assertTrue(form.is_valid())


	def test_form_invalid(self):
		data = { 'category': ['Adventure', 'Animation', 'Anime', 'War'] }
		form = MovieCategoryForm(data=data)
		self.assertFalse(form.is_valid())












