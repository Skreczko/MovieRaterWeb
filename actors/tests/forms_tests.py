from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from actors.models import Actor, ActorComment, ActorGallery, ActorRole, CrewRole
from actors.forms import ActorForm, ActorCommentForm, ActorCastForm
from accounts.models import MyUser
from movies.models import Movie
import datetime


# Create your tests here.

class ActorTestCase(TestCase):
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
									biography=biography,
									born=born,
									if_died=if_died,
									is_crew=is_crew,
									)

	def test_actor_valid_form(self):
		actor = self.create_actor()
		data = {'name': actor.name,
				"last_name": actor.last_name,
				"original_name": actor.original_name,
				"nationality": actor.nationality,
				"city_of_birth": actor.city_of_birth,
				"biography": actor.biography,
				"born": actor.born,
				"if_died": actor.if_died,
				"is_crew": actor.is_crew,
				}
		form = ActorForm(data=data)
		self.assertTrue(form.is_valid())
		self.assertEqual(form.cleaned_data.get('name'), actor.name)
		self.assertEqual(form.cleaned_data.get("last_name"), actor.last_name)
		self.assertEqual(form.cleaned_data.get("original_name"), actor.original_name)
		self.assertEqual(form.cleaned_data.get("nationality"), actor.nationality)
		self.assertEqual(form.cleaned_data.get("city_of_birth"), actor.city_of_birth)
		self.assertEqual(form.cleaned_data.get("biography"), actor.biography)
		self.assertEqual(form.cleaned_data.get("born"), actor.born)
		self.assertEqual(form.cleaned_data.get("if_died"), actor.if_died)
		self.assertEqual(form.cleaned_data.get("is_crew"), actor.is_crew)


	def test_actor_invalid_form(self):
		actor = self.create_actor()
		data = {'name': "",
				"last_name": actor.last_name,
				"original_name": actor.original_name,
				"nationality": actor.nationality,
				"city_of_birth": actor.city_of_birth,
				"biography": actor.biography,
				"born": actor.born,
				"if_died": actor.if_died,
				"is_crew": actor.is_crew,
				}
		form = ActorForm(data=data)
		self.assertFalse(form.is_valid())
		self.assertNotEqual(form.cleaned_data.get('title'), actor.name)

	def test_actor_comment_valid_form(self):
		actor = self.create_actor()
		actcom = ActorComment.objects.create(actor=actor, comment='Comment for Emily', stars=3)
		data = {'comment': actcom.comment,
				"stars": actcom.stars, }
		form = ActorCommentForm(data=data)
		self.assertTrue(form.is_valid())
		self.assertEqual(form.cleaned_data.get('comment'), actcom.comment)
		self.assertEqual(form.cleaned_data.get("stars"), actcom.stars)

		self.assertNotEqual(form.cleaned_data.get('comment'), 'Some random comment')
		self.assertNotEqual(form.cleaned_data.get("stars"), 5)

	def test_actor_comment_invalid_form(self):
		actor = self.create_actor()
		actcom = ActorComment.objects.create(actor=actor, comment='Comment for Emily', stars=3)
		data = {'comment': actcom.comment,
				"stars": 6}
		form = ActorCommentForm(data=data)
		self.assertFalse(form.is_valid())

	def test_actor_cast_valid_form(self):
		actor = self.create_actor()
		movie = self.create_movie()
		actor_role = ActorRole.objects.create(actor=actor, movie=movie, role="First role")
		data = {'movie': actor_role.movie.id,
				"role": actor_role.role,
				}
		form = ActorCastForm(data=data)
		self.assertTrue(form.is_valid())
		self.assertEqual(form.cleaned_data.get('movie'), movie)
		self.assertEqual(form.cleaned_data.get("role"), "First role")





