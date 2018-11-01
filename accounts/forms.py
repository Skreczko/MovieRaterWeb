from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.db.models import Q

from .models import MyUser
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from .models import REGEX_FOR_USER

User = get_user_model()

class UserLoginForm(forms.Form):
    query = forms.CharField(label='Username or Email',
                                # validators = [RegexValidator(
                                # regex = REGEX_FOR_USER,
                                # message = 'Username must be alphanumeric',
                                # code = 'invalid_username')]
                               )
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        query = self.cleaned_data.get('query')
        password = self.cleaned_data.get('password')
        query_user = User.objects.filter(
                        Q(username__iexact=query)|
                        Q(email__iexact=query)
                        ).distinct()
        if not query_user.exists() and query_user != 1:
            raise forms.ValidationError('Invalid username/email or password')
        user_obj = query_user.first()
        if not user_obj.check_password(password):
            raise forms.ValidationError('Invalid username/email or password')
        if not user_obj.is_active:
            raise forms.ValidationError('Please activate your account')
        self.cleaned_data['user_obj'] = user_obj
        return super(UserLoginForm,self).clean(*args, **kwargs)


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('username', 'email', )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('username', 'email', 'is_staff', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]