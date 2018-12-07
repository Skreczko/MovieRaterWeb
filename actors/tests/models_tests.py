from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from actors.models import Actor, ActorComment, ActorGallery, ActorRole, CrewRole
from movies.models import Movie
from accounts.models import MyUser
import os
import datetime
# Create your tests here.

class ActorModelTestCase(TestCase):
	def setUp(self):
		Actor.objects.create(
			name='Emily',
			last_name='Konawsky',
			original_name='Emily Konawsky-Butt',
			nationality='US',
			city_of_birth='LA',
			photo=SimpleUploadedFile("file.jpg", b"file_content", content_type='image/jpeg'),
			biography='Some random biography',
			born=datetime.date(1985,5,25),
			if_died=False,
			is_crew=True
			)


	def create_actor(self,
					 name='Emily',
					 last_name='Konawsky',
					 original_name='Emily Konawsky-Butt',
					 nationality='US',
					 city_of_birth='LA',
					 photo=SimpleUploadedFile("file.jpg", b"file_content", content_type='image/jpeg'),
					 biography='Some random biography',
					 born=datetime.date(1985,5,25),
					 if_died=False,
					 is_crew=True
					 ):
		return Actor.objects.create(name=name,
									last_name=last_name,
									original_name=original_name,
									nationality=nationality,
									city_of_birth=city_of_birth,
									photo=photo,
									biography=biography,
									born=born,
									if_died=if_died,
									is_crew=is_crew,
									)


	def create_user(self,
					username='User1',
					email='user1@gmail.com',
					is_active = True,
					is_admin = False,
					is_staff = False,
					):
		return MyUser.objects.create(
			username=username,
			email=email,
			is_active=is_active,
			is_admin=is_admin,
			is_staff=is_staff
			)
	def create_movie(self,
			title='Robin Hood',
			year_of_production=2018,
			production='US',
			budget=48027682,
			poster=SimpleUploadedFile("file.jpg", b"file_content", content_type='image/jpeg'),
			duration=104,
			description='Movie about Robin Hood.'
					 ):
		return Movie.objects.create(title=title,
									year_of_production=year_of_production,
									production=production,
									budget=budget,
									poster=poster,
									duration=duration,
									description=description
									)


	def test_name_lastname(self):
		obj = Actor.objects.get(slug='konawsky-emily')
		self.assertEqual(obj.name +" "+ obj.last_name, 'Emily Konawsky')

	def test_slugify(self):
		obj1 = self.create_actor()
		obj2 = self.create_actor()
		obj3 = self.create_actor()

		self.assertNotEqual(obj1.slug, obj2.slug)
		self.assertNotEqual(obj2.slug, obj3.slug)
		self.assertNotEqual(obj1.slug, obj3.slug)


	def test_actor_photo(self):
		photo_actor1 = self.create_actor().photo.name
		photo_actor2 = self.create_actor().photo.name
		self.assertNotEqual(photo_actor1, photo_actor2)

		photo_actor1 = self.create_actor()
		photo_actor2 = self.create_actor()
		self.assertNotEqual(os.path.basename(photo_actor1.photo.name),
							os.path.basename(photo_actor2.photo.name))


	def test_actor_age(self):
		age_actor1 = self.create_actor().actor_age
		self.assertEqual(age_actor1, 33)



	def test_comments(self):
		actor = self.create_actor()
		user1 = self.create_user()
		user2 = self.create_user(username='User2', email='user2@gmail.com')

		comment1 = ActorComment.objects.create(
			added_by=user1,
			actor=actor,
			comment='Random comment',
			stars='3'
			)
		comment2 = ActorComment.objects.create(
			added_by=user2,
			actor=actor,
			comment='Random comment 2',
			stars='2',
			)

		self.assertEqual(ActorComment.objects.all().count(), 2)
		rating, rates_amount = actor.average_stars()
		self.assertEqual(rating, 2.5)
		self.assertEqual(rates_amount, 2)
	#
	#
	def test_gallery(self):
		actor1 = self.create_actor()
		actor2 = self.create_actor()
		image = SimpleUploadedFile("file.jpg", b"file_content", content_type='image/jpeg')
		image1 = ActorGallery.objects.create(actor=actor1, picture=image)
		image2 = ActorGallery.objects.create(actor=actor1, picture=image)
		image3 = ActorGallery.objects.create(actor=actor2, picture=image)

		self.assertEqual(ActorGallery.objects.all().count(), 3)
		self.assertEqual(ActorGallery.objects.filter(actor=actor1).count(), 2)

		self.assertNotEqual(os.path.basename(image1.picture.name), os.path.basename(image2.picture.name))
		self.assertNotEqual(os.path.basename(image1.picture.name), os.path.basename(image3.picture.name))
		self.assertNotEqual(os.path.basename(image2.picture.name), os.path.basename(image3.picture.name))

	def test_actor_role(self):
		actor= self.create_actor()
		movie = self.create_movie()
		picture = SimpleUploadedFile("file.jpg", b"file_content", content_type='image/jpeg')
		role = ActorRole.objects.create(
			movie=movie,
			actor=actor,
			role='First role',
			picture = picture,)

		self.assertEqual(ActorRole.objects.all().count(), 1)
		self.assertNotEqual(os.path.basename(role.picture.name), "file.jpg")
		self.assertEqual(len(os.path.basename(role.picture.name)), 13)    #9 for name and 4 for ".jpg"
		self.assertEqual(str(role), 'Robin Hood (2018) - Emily Konawsky - First role')

	def test_crew_role(self):
		actor= self.create_actor()
		movie = self.create_movie()
		picture = SimpleUploadedFile("file.jpg", b"file_content", content_type='image/jpeg')
		role = CrewRole.objects.create(
			movie=movie,
			actor=actor,
			role='First role',
			picture = picture,)

		self.assertEqual(CrewRole.objects.all().count(), 1)
		self.assertNotEqual(os.path.basename(role.picture.name), "file.jpg")
		self.assertEqual(len(os.path.basename(role.picture.name)), 13)    #9 for name and 4 for ".jpg"
		self.assertEqual(str(role), 'Robin Hood (2018) - Emily Konawsky - First role')
