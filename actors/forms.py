from django import forms
from .models import Actor, ActorComment, ActorRole



YEARS = [x for x in range(1930, 2041)]

class ActorForm(forms.ModelForm):

	class Meta:

		model = Actor
		fields = ['name', 'last_name', 'photo', 'nationality', 'city_of_birth', 'biography', 'born', 'if_died', 'died']

		widgets = {
			'born': forms.SelectDateWidget(years=YEARS),
			'died': forms.SelectDateWidget(years=YEARS),

		}


class ActorCommentForm(forms.ModelForm):
	class Meta:
		model = ActorComment
		fields = ['comment' ]


class MovieCastForm(forms.ModelForm):
	class Meta:
		model = ActorRole
		fields = ['actor', 'role', 'picture']

class MovieCastRoleForm(forms.ModelForm):
	class Meta:
		model = ActorRole
		fields = ['role', 'picture']


