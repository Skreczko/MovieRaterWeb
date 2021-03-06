from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from actors.models import Actor, ActorComment, ActorGallery, ActorRole, CrewRole
from movies.models import Movie
from accounts.models import MyUser
import datetime

# Create your tests here.

class ActorTestCase(TestCase):
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

	def test_actor_list_view(self):
		list_url = reverse("actor_list")
		response = self.client.get(list_url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(list_url, '/persons/')

	def test_actor_create_view(self):
		list_url = reverse("actor_create")
		response = self.client.get(list_url)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(list_url, '/persons/add/')

	def test_actor_detail_view(self):
		actor = self.create_actor()
		response = self.client.get(actor.get_to_detail())
		self.assertEqual(response.status_code, 200)

		actor_edit_url = actor.get_to_detail()
		response = self.client.get(actor_edit_url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(actor_edit_url, '/persons/detail/konawsky-emily/')

	def test_actor_update_view(self):
		actor = self.create_actor()
		actor_edit_url = reverse("actor_update", kwargs={"slug": actor.slug})
		response = self.client.get(actor_edit_url)
		self.assertEqual(response.status_code, 302)

		actor_edit_url = actor.get_to_detail() + 'edit/'
		response = self.client.get(actor_edit_url)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(actor_edit_url, '/persons/detail/konawsky-emily/edit/')

	def test_actor_delete_view(self):
		actor = self.create_actor()
		actor_delete_url = reverse("movie_delete", kwargs={"slug": actor.slug})
		response = self.client.get(actor_delete_url)
		self.assertEqual(response.status_code, 302)

		actor_delete_url = actor.get_to_detail() + 'delete/'
		response = self.client.get(actor_delete_url)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(actor_delete_url, '/persons/detail/konawsky-emily/delete/')

	def test_actor_gallery_list(self):
		actor = self.create_actor()
		gallery_list = reverse("actor_gallery", kwargs={"slug":actor.slug})
		response = self.client.get(gallery_list)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(gallery_list, '/persons/detail/konawsky-emily/gallery/')

	def test_actor_gallery_add(self):
		actor = self.create_actor()
		gallery_add = reverse("add_actor_picture", kwargs={"slug":actor.slug})
		response = self.client.get(gallery_add)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(gallery_add, '/persons/detail/konawsky-emily/gallery/add_image/')

	def test_actor_gallery_management(self):
		actor = self.create_actor()
		gallery_list = reverse("actor_management_picture", kwargs={"slug":actor.slug})
		response = self.client.get(gallery_list)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(gallery_list, '/persons/detail/konawsky-emily/gallery/management_image/')

	def test_actor_gallery_delete(self):
		actor = self.create_actor()
		image = SimpleUploadedFile("file.jpg", b"file_content", content_type='image/jpeg')
		actor_gallery = ActorGallery.objects.create(actor=actor, picture=image)
		gallery_delete = reverse("delete_actor_picture", kwargs={"slug":actor.slug, "id":actor_gallery.id})
		response = self.client.get(gallery_delete)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(gallery_delete, '/persons/detail/konawsky-emily/gallery/delete/1')

	def test_actor_cast_list(self):
		actor = self.create_actor()
		movie = self.create_movie()
		picture = SimpleUploadedFile("file.jpg", b"file_content", content_type='image/jpeg')
		cast = ActorRole.objects.create(
			movie=movie,
			actor=actor,
			role='First role',
			picture=picture, )
		cast_list = reverse("actor_cast_list", kwargs={"slug":actor.slug})
		response = self.client.get(cast_list)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(cast_list, '/persons/detail/konawsky-emily/cast/')

	def test_actor_cast_add_role(self):
		actor = self.create_actor()
		movie = self.create_movie()
		picture = SimpleUploadedFile("file.jpg", b"file_content", content_type='image/jpeg')
		cast = ActorRole.objects.create(
			movie=movie,
			actor=actor,
			role='First role',
			picture=picture, )
		cast_add = reverse("actor_add_cast", kwargs={"slug":actor.slug})
		response = self.client.get(cast_add)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(cast_add, '/persons/detail/konawsky-emily/cast/add_role/')

	def test_actor_cast_edit(self):
		actor = self.create_actor()
		movie = self.create_movie()
		picture = SimpleUploadedFile("file.jpg", b"file_content", content_type='image/jpeg')
		cast = ActorRole.objects.create(
			movie=movie,
			actor=actor,
			role='First role',
			picture=picture, )
		cast_edit = reverse("actor_edit_cast", kwargs={"slug":actor.slug,"id":cast.id})
		response = self.client.get(cast_edit)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(cast_edit, '/persons/detail/konawsky-emily/cast/edit/1/')

	def test_actor_cast_delete(self):
		actor = self.create_actor()
		movie = self.create_movie()
		picture = SimpleUploadedFile("file.jpg", b"file_content", content_type='image/jpeg')
		cast = ActorRole.objects.create(
			movie=movie,
			actor=actor,
			role='First role',
			picture=picture, )
		cast_delete = reverse("actor_delete_cast", kwargs={"slug":actor.slug, "id":cast.id})

		response = self.client.get(cast_delete)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(cast_delete, '/persons/detail/konawsky-emily/cast/delete/1/')

	def test_actor_crew_list(self):
		actor = self.create_actor()
		crew_list = reverse("actor_crew_list", kwargs={"slug":actor.slug})
		response = self.client.get(crew_list)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(crew_list, '/persons/detail/konawsky-emily/crew/')

	def test_actor_crew_add_role(self):
		actor = self.create_actor()
		crew_add = reverse("actor_add_crew", kwargs={"slug":actor.slug})
		response = self.client.get(crew_add)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(crew_add, '/persons/detail/konawsky-emily/crew/add_role/')

	def test_actor_crew_edit(self):
		actor = self.create_actor()
		movie = self.create_movie()
		picture = SimpleUploadedFile("file.jpg", b"file_content", content_type='image/jpeg')
		crew = CrewRole.objects.create(
			movie=movie,
			actor=actor,
			role='First role',
			picture=picture, )
		crew_edit = reverse("actor_edit_crew", kwargs={"slug":actor.slug, "id":crew.id})
		response = self.client.get(crew_edit)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(crew_edit, '/persons/detail/konawsky-emily/crew/edit/1/')

	def test_actor_crew_delete(self):
		actor = self.create_actor()
		movie = self.create_movie()
		picture = SimpleUploadedFile("file.jpg", b"file_content", content_type='image/jpeg')
		crew = CrewRole.objects.create(
			movie=movie,
			actor=actor,
			role='First role',
			picture=picture, )
		crew_delete = reverse("actor_delete_crew", kwargs={"slug":actor.slug, "id":crew.id})
		response = self.client.get(crew_delete)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(crew_delete, '/persons/detail/konawsky-emily/crew/delete/1/')

	def test_actor_comment_list(self):
		actor = self.create_actor()
		user1 = MyUser.objects.create(
					username='User1',
					email='user1@gmail.com',
					is_active = True,
					is_admin = False,
					is_staff = False,)
		comment1 = ActorComment.objects.create(
			added_by=user1,
			actor=actor,
			comment='Random comment',
			stars='3',
		)
		comment_list = reverse('actor_comment_list', kwargs={"slug":actor.slug})
		response = self.client.get(comment_list)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(comment_list, '/persons/detail/konawsky-emily/comments/')

	def test_actor_comment_add(self):
		actor = self.create_actor()
		comment_add = reverse('actor_add_comment', kwargs={"slug":actor.slug})
		response = self.client.get(comment_add)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(comment_add, '/persons/detail/konawsky-emily/comments/add_comment/')

	def test_actor_comment_edit(self):
		actor = self.create_actor()
		user1 = MyUser.objects.create(
					username='User1',
					email='user1@gmail.com',
					is_active = True,
					is_admin = False,
					is_staff = False,)
		comment1 = ActorComment.objects.create(
			added_by=user1,
			actor=actor,
			comment='Random comment',
			stars='3',
		)
		comment_edit = reverse("actor_edit_comment", kwargs={"pk":comment1.id})
		print(comment_edit)
		response = self.client.get(comment_edit)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(comment_edit, '/persons/detail/comments/edit_comment/1')


	def test_actor_comment_delete(self):
		actor = self.create_actor()
		user1 = MyUser.objects.create(
					username='User1',
					email='user1@gmail.com',
					is_active = True,
					is_admin = False,
					is_staff = False,)
		comment1 = ActorComment.objects.create(
			added_by=user1,
			actor=actor,
			comment='Random comment',
			stars='3',
		)
		comment_delete = reverse("actor_delete_comment", kwargs={"pk":comment1.id})
		response = self.client.get(comment_delete)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(comment_delete, '/persons/detail/comments/delete_comment/1')









