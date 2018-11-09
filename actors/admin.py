from django.contrib import admin
from .forms import ActorForm
from .models import Actor, ActorComment
from django.utils.safestring import mark_safe
# Register your models here.

class ActorAdmin(admin.ModelAdmin):
	list_display = ['name',  'last_name', 'is_photo' , 'is_biography']
	list_filter = ['name', 'last_name',]
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




admin.site.register(Actor, ActorAdmin)
admin.site.register(ActorComment, ActorCommentAdmin)
