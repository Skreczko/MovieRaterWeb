from django import forms
from .models import Actor, ActorComment



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
		fields = ['actor', 'comment', 'stars']




