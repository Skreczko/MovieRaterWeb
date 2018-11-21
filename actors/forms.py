from django import forms
from .models import YEARS, YES_NO
from .models import Actor, ActorComment, ActorRole





class ActorForm(forms.ModelForm):

	class Meta:

		model = Actor
		fields = ['is_crew', 'name', 'last_name', 'photo', 'nationality', 'city_of_birth', 'biography', 'born', 'if_died', 'died', ]

		widgets = {
			'born': forms.SelectDateWidget(years=YEARS),
			'died': forms.SelectDateWidget(years=YEARS),
			'is_crew': forms.Select(choices=YES_NO),

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


