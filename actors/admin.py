from django.contrib import admin
from .forms import ActorForm
from .models import Actor, ActorComment, ActorGallery, ActorRole, CrewRole
from django.utils.safestring import mark_safe
# Register your models here.

class ActorAdmin(admin.ModelAdmin):
	list_display = ['name',  'last_name','is_crew_member', 'is_photo', 'is_biography']
	list_filter = ['is_crew', 'name', 'last_name',]
	search_fields = ['name', 'last_name']
	readonly_fields = ['slug', 'show_photo']
	list_per_page = 50

	form = ActorForm

	def is_photo(self, obj, *args, **kwargs):
		if obj.photo:
			return True
		else:
			return False
	is_photo.boolean = True

	def is_biography(self, obj, *args, **kwargs):
		if obj.biography:
			return True
		else:
			return False
	is_biography.boolean = True

	def is_crew_member(self, obj, *args, **kwargs):
		return obj.is_crew
	is_crew_member.boolean = True


	def show_photo(self, obj):
		return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
			url=obj.photo.url,
			width=120,
			height=240,))

class ActorCommentAdmin(admin.ModelAdmin):
	list_display = ['actor', 'stars', 'is_comment', 'added_time', 'edited_time']
	readonly_fields = ['added_time', 'edited_time']
	list_filter = ['actor', 'publish_date', 'edited_date']

	class Meta:
		model = ActorComment

	def is_comment(self, obj, *args, **kwargs):
		if obj.comment:
			return True
		else:
			return False
	is_comment.boolean = True

class ActorGalleryAdmin(admin.ModelAdmin):
	list_display = ['actor', 'picture', 'show_photo']
	search_fields = ['actor']
	list_per_page = 50

	class Meta:
		model = ActorGallery

	def show_photo(self, obj):
		return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
			url=obj.picture.url,
			width=50,
			height=60,))


class ActorRoleAdmin(admin.ModelAdmin):
	list_display = ['movie', 'actor', 'role', 'is_picture']
	search_fields = ['movie', 'actor', 'role']
	readonly_fields = ['show_photo']
	list_per_page = 50

	class Meta:
		model = ActorRole

	def is_picture(self, obj, *args, **kwargs):
		if obj.picture:
			return True
		else:
			return False
	is_picture.boolean = True

	def show_photo(self, obj):
		return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
			url=obj.picture.url,
			width=50,
			height=60,))


class CrewRoleAdmin(admin.ModelAdmin):
	list_display = ['movie', 'actor', 'role', 'is_picture']
	search_fields = ['movie', 'actor', 'role']
	readonly_fields = ['show_photo']
	list_per_page = 50

	class Meta:
		model = CrewRole

	def is_picture(self, obj, *args, **kwargs):
		if obj.picture:
			return True
		else:
			return False
	is_picture.boolean = True

	def show_photo(self, obj):
		return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
			url=obj.picture.url,
			width=50,
			height=60,))


admin.site.register(Actor, ActorAdmin)
admin.site.register(ActorComment, ActorCommentAdmin)
admin.site.register(ActorGallery, ActorGalleryAdmin)
admin.site.register(ActorRole, ActorRoleAdmin)
admin.site.register(CrewRole, CrewRoleAdmin)
