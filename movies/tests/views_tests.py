from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from movies.models import Movie, MovieCategory, MovieComment, MovieGallery
from accounts.models import MyUser
import os
from django.utils.text import slugify
# Create your tests here.

class MovieTestCase(TestCase):
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

	def test_movie_list_view(self):
		list_url = reverse("movie_list")
		response = self.client.get(list_url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(list_url, '/movies/')

	def test_movie_create_view(self):
		list_url = reverse("movie_create")
		response = self.client.get(list_url)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(list_url, '/movies/add/')

	def test_movie_detail_view(self):
		movie = self.create_movie()
		response = self.client.get(movie.get_to_detail())
		self.assertEqual(response.status_code, 200)

		movie_edit_url = movie.get_to_detail()
		response = self.client.get(movie_edit_url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(movie_edit_url, '/movies/detail/robin-hood')

	def test_movie_update_view(self):
		movie = self.create_movie()
		movie_edit_url = reverse("movie_update", kwargs={"slug": movie.slug})
		response = self.client.get(movie_edit_url)
		self.assertEqual(response.status_code, 302)

		movie_edit_url = movie.get_to_detail() + '/edit/'
		response = self.client.get(movie_edit_url)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(movie_edit_url, '/movies/detail/robin-hood/edit/')

	def test_movie_delete_view(self):
		movie = self.create_movie()
		movie_delete_url = reverse("movie_delete", kwargs={"slug": movie.slug})
		response = self.client.get(movie_delete_url)
		self.assertEqual(response.status_code, 302)

		movie_delete_url = movie.get_to_detail() + '/delete/'
		response = self.client.get(movie_delete_url)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(movie_delete_url, '/movies/detail/robin-hood/delete/')

	def test_movie_category_edit(self):
		movie = self.create_movie()
		category_edit = reverse("category_edit", kwargs={"slug": movie.slug})
		response = self.client.get(category_edit)
		self.assertEqual(response.status_code, 302)

		category_edit = movie.get_to_detail() + '/edit_category/'
		response = self.client.get(category_edit)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(category_edit, '/movies/detail/robin-hood/edit_category/' )

	def test_movie_category_add(self):
		movie = self.create_movie()
		cat_add_url = reverse("add_category", kwargs={"slug" : movie.slug})
		response = self.client.get(cat_add_url)
		self.assertEqual(response.status_code, 302)

		cat_add_url = movie.get_to_detail() + '/add_category/'
		response = self.client.get(cat_add_url)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(cat_add_url, '/movies/detail/robin-hood/add_category/')

	def test_movie_gallery_list(self):
		movie = self.create_movie()
		gallery_list = reverse("picture_gallery", kwargs={"slug":movie.slug})
		response = self.client.get(gallery_list)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(gallery_list, '/movies/detail/robin-hood/gallery/')

	def test_movie_gallery_add(self):
		movie = self.create_movie()
		gallery_add = reverse("add_picture", kwargs={"slug":movie.slug})
		response = self.client.get(gallery_add)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(gallery_add, '/movies/detail/robin-hood/gallery/add_image/')

	def test_movie_gallery_management(self):
		movie = self.create_movie()
		gallery_list = reverse("management_picture", kwargs={"slug":movie.slug})
		response = self.client.get(gallery_list)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(gallery_list, '/movies/detail/robin-hood/gallery/management_image/')

	def test_movie_gallery_delete(self):
		movie = self.create_movie()
		image = SimpleUploadedFile("file.jpg", b"file_content", content_type='image/jpeg')
		movie_gallery = MovieGallery.objects.create(movie=movie, picture=image)
		gallery_delete = reverse("delete_picture", kwargs={"slug":movie.slug, "id":movie_gallery.id})
		response = self.client.get(gallery_delete)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(gallery_delete, '/movies/detail/robin-hood/gallery/delete/1')

	def test_movie_comment_list(self):
		movie = self.create_movie()
		user1 = MyUser.objects.create(
					username='User1',
					email='user1@gmail.com',
					is_active = True,
					is_admin = False,
					is_staff = False,)
		comment1 = MovieComment.objects.create(
			added_by=user1,
			movie=movie,
			comment='Random comment',
			stars='3',
		)
		comment_list = reverse('comment_list', kwargs={"slug":movie.slug})
		response = self.client.get(comment_list)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(comment_list, '/movies/detail/robin-hood/comments/')

	def test_movie_comment_add(self):
		movie = self.create_movie()
		comment_add = reverse('add_comment', kwargs={"slug":movie.slug})
		response = self.client.get(comment_add)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(comment_add, '/movies/detail/robin-hood/comments/add_comment/')

	def test_movie_comment_edit(self):
		movie = self.create_movie()
		user1 = MyUser.objects.create(
					username='User1',
					email='user1@gmail.com',
					is_active = True,
					is_admin = False,
					is_staff = False,)
		comment1 = MovieComment.objects.create(
			added_by=user1,
			movie=movie,
			comment='Random comment',
			stars='3',
		)
		comment_edit = reverse("edit_comment", kwargs={"pk":comment1.id})
		response = self.client.get(comment_edit)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(comment_edit, '/movies/detail/comments/edit_comment/1')


	def test_movie_comment_delete(self):
		movie = self.create_movie()
		user1 = MyUser.objects.create(
					username='User1',
					email='user1@gmail.com',
					is_active = True,
					is_admin = False,
					is_staff = False,)
		comment1 = MovieComment.objects.create(
			added_by=user1,
			movie=movie,
			comment='Random comment',
			stars='3',
		)
		comment_delete = reverse("delete_comment", kwargs={"pk":comment1.id})
		response = self.client.get(comment_delete)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(comment_delete, '/movies/detail/comments/delete_comment/1')










