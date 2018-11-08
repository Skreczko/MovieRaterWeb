from django.contrib import admin
from .forms import ActorForm
from .models import Actor, ActorComment
# Register your models here.

class ActorAdmin(admin.ModelAdmin):
	list_display = ['name',  'last_name', 'is_photo' , 'is_biography']
	list_filter = ['name', 'last_name' ]
	readonly_fields = ['slug']

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





admin.site.register(Actor, ActorAdmin)
admin.site.register(ActorComment)
