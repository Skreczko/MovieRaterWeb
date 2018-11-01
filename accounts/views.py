from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UserCreationForm,UserLoginForm
from .models import ActivateProfile
from django.contrib.auth import login, logout, get_user_model
# Create your views here.

User = get_user_model()

def homepage(request):
    if request.user.is_authenticated():
        pass
    return render(request, "home.html", {})

def register(request, *args, **kwargs):
    form = UserCreationForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
    return render(request, "accounts/register.html", {"form":form})

def user_login(request, *args, **kwargs):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        user_obj = form.cleaned_data.get('user_obj')
        login(request, user_obj)
        return HttpResponseRedirect("/")
    return render(request, "login.html", {"form":form})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def activate_user(request, code=None, *args, **kwargs):
    if code:
        query_code = ActivateProfile.objects.filter(key=code)
        if query_code.exists() :
            act_user = query_code.first()
            if not act_user.expired:
                user_obj = act_user.user
                user_obj.is_active = True
                user_obj.save()
                act_user.expired = True
                act_user.save()
                return HttpResponseRedirect('/login')
    return HttpResponseRedirect('/login')

