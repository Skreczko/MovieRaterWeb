from django import forms
from .models import Actor, ActorComment


YEARS = [x for x in range(1930,2041)]


class ActorForm(forms.ModelForm):
	birth = forms.DateField(widget=forms.SelectDateWidget(years=YEARS))

	class Meta:
		model = Actor
		fields = ['name', 'last_name', 'photo', 'biography', 'birth']


class ActorCommentForm(forms.ModelForm):

	class Meta:
		model = ActorComment
		fields = ['actor', 'comment', 'stars']




