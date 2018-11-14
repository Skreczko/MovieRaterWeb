from django.contrib import admin
from .models import Movie,  MovieComment, MovieGallery, MovieCategory
from .forms import MovieForm, MovieCategoryForm
from django.utils.safestring import mark_safe
# Register your models here.

class MovieAdmin(admin.ModelAdmin):
	list_display = ['title',  'year_of_production',  'is_poster', ]
	list_filter = ['year_of_production', ]
	search_fields = ['title' ,  'year_of_production']
	readonly_fields = ['slug', 'show_poster']
	list_per_page = 50

	form = MovieForm

	def is_poster(self, obj, *args, **kwargs):
		if obj.poster:
			return True
		else:
			return False
	is_poster.boolean = True

	def show_poster(self, obj):
		return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
			url=obj.poster.url,
			width=120,
			height=240,))


class MovieCommentAdmin(admin.ModelAdmin):
	list_display = ['movie', 'stars', 'is_comment', 'added_time', 'edited_time']
	readonly_fields = ['added_time', 'edited_time']
	list_filter = ['movie', 'publish_date', 'edited_date']

	class Meta:
		model = MovieComment

	def is_comment(self, obj, *args, **kwargs):
		if obj.comment:
			return True
		else:
			return False
	is_comment.boolean = True

class MovieGalleryAdmin(admin.ModelAdmin):
	list_display = ['movie', 'picture', 'show_photo']
	search_fields = ['movie']
	list_per_page = 50

	class Meta:
		model = MovieGallery

	def show_photo(self, obj):
		return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
			url=obj.picture.url,
			width=50,
			height=60,))



class MovieCategoryAdmin(admin.ModelAdmin):
	list_display = ['category' ]

	form = MovieCategoryForm


admin.site.register(Movie, MovieAdmin)
admin.site.register(MovieComment, MovieCommentAdmin)
admin.site.register(MovieGallery, MovieGalleryAdmin)
admin.site.register(MovieCategory)
