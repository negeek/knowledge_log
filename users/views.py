from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from .forms import RegistrationForm

# Create your views here.


def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('logs:index'))


def register(request):
    if request.method != 'POST':
        form = RegistrationForm()
    else:
        print(request.POST)
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            print(new_user)

            # authenticated_user = authenticate(
            # username=new_user.username, password=request.POST['password1'])
            #login(request, authenticated_user)
            return HttpResponseRedirect(reverse('users:login'))
            # return HttpResponseRedirect(reverse('logs:index'))
    return render(request, 'registration/register.html', {'form': form})
