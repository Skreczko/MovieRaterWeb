from django import forms
from .models import YEARS, YES_NO, CREW_ROLE
from .models import Actor, ActorGallery, ActorComment, ActorRole, CrewRole





class ActorForm(forms.ModelForm):
	class Meta:
		model = Actor
		fields = ['is_crew', 'name', 'last_name', 'original_name', 'photo', 'nationality',
				  'city_of_birth', 'biography', 'born', 'if_died', 'died', ]

		widgets = {
			'born': forms.SelectDateWidget(years=YEARS),
			'died': forms.SelectDateWidget(years=YEARS),
			'is_crew': forms.Select(choices=YES_NO),

		}


class ActorCommentForm(forms.ModelForm):
	class Meta:
		model = ActorComment
		fields = ['comment', 'stars']

		widgets = {
			'comment': forms.Textarea

		}



class ActorStarsForm(forms.Form):
	stars = forms.IntegerField()

class ActorGalleryForm(forms.ModelForm):
	class Meta:
		model = ActorGallery
		fields = ['picture']


					#MOVIE SECTION

class MovieCastForm(forms.ModelForm):
	class Meta:
		model = ActorRole
		fields = ['actor', 'role', 'picture']

class MovieCastRoleForm(forms.ModelForm):
	class Meta:
		model = ActorRole
		fields = ['role', 'picture']

class MovieCrewForm(forms.ModelForm):
	class Meta:
		model = CrewRole
		fields = ['actor', 'role', 'picture']

class MovieCrewRoleForm(forms.ModelForm):
	class Meta:
		model = CrewRole
		fields = ['role', 'picture']

					#ACTOR SECTION
class ActorCastForm(forms.ModelForm):
	class Meta:
		model = ActorRole
		fields = ['movie', 'role', 'picture']


class ActorCrewForm(forms.ModelForm):
	class Meta:
		model = CrewRole
		fields = ['movie', 'role', 'picture']

		widgets = {
			'role': forms.Select(choices=CREW_ROLE),

		}


