from django.test import TestCase
from .models import Movie, MovieCategory, MovieComment
from accounts.models import MyUser
from django.utils.text import slugify
# Create your tests here.

class MovieModelTestCase(TestCase):
	def setUp(self):
		Movie.objects.create(
			title='Robin Hood',
			year_of_production='2018',
			production='US',
			budget='48027682',
			duration='104',
			description='Movie about Robin Hood.'
		)

	def create_movie(self,
			title='Robin Hood',
			year_of_production='2018',
			production='US',
			budget='48027682',
			duration='104',
			description='Movie about Robin Hood.'
					 ):
		return Movie.objects.create(title=title,
									year_of_production=year_of_production,
									production=production,
									budget=budget,
									duration=duration,
									description=description
									)

	def create_user(self,
					username='User1',
					email='user1@gmail.com',
					is_active = True,
					is_admin = False,
					is_staff = False,
					):
		return MyUser.objects.create(username=username,
									 email=email,
									 is_active=is_active,
									 is_admin=is_admin,
									 is_staff=is_staff)

	def test_title(self):
		obj = Movie.objects.get(slug='robin-hood')
		self.assertEqual(obj.title, 'Robin Hood')

	def test_slugify(self):
		title = 'Avatar'
		obj1 = self.create_movie(title=title)
		obj2 = self.create_movie(title=title)
		obj3 = self.create_movie(title=title)
		slug = slugify(title)
		self.assertEqual(obj1.slug, slug)
		self.assertNotEqual(obj2.slug, slug)
		self.assertNotEqual(obj2.slug, obj3.slug)

	def test_categories(self):
		cat_action = MovieCategory.objects.create(category='Action')
		cat_fantasy = MovieCategory.objects.create(category='Fantasy')
		cat_war = MovieCategory.objects.create(category='War')
		cat_thriller = MovieCategory.objects.create(category='Thriller')
		self.assertEqual(MovieCategory.objects.all().count(), 4)

		movie = self.create_movie()
		cat_action.related_movie.add(movie)
		cat_fantasy.related_movie.add(movie)
		cat_war.related_movie.add(movie)

		count = MovieCategory.objects.filter(related_movie=movie).count()
		self.assertEqual(count, 3)



	def test_comments(self):
		movie = self.create_movie()
		user1 = self.create_user()
		user2 = self.create_user(username='User2', email='user2@gmail.com')

		comment1 = MovieComment.objects.create(added_by=user1,
											   movie=movie,
											   comment='Random comment',
											   stars='3'
											   )
		comment2 = MovieComment.objects.create(added_by=user2,
											   movie=movie,
											   comment='Random comment 2',
											   stars='2',
											   )

		self.assertEqual(MovieComment.objects.all().count(), 2)
		rating, rates_amount = movie.average_stars
		self.assertEqual(rating, 2.5)
		self.assertEqual(rates_amount, 2)







