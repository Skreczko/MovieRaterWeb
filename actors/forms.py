from django import forms
from .models import Actor, ActorComment


YEARS = [x for x in range(1930,2041)]


class ActorForm(forms.ModelForm):
	born = forms.DateField(widget=forms.SelectDateWidget(years=YEARS))
	died = forms.DateField(widget=forms.SelectDateWidget(years=YEARS), help_text="If actor is still alive, leave it")

	class Meta:
		model = Actor
		fields = ['name', 'last_name', 'photo', 'nationality', 'city_of_birth', 'biography', 'born', 'if_died', 'died']


class ActorCommentForm(forms.ModelForm):

	class Meta:
		model = ActorComment
		fields = ['actor', 'comment', 'stars']




