
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm
from django.contrib.auth.models import Group



def login_view(request):

    if request.user.is_authenticated:
        return redirect("portfolio")

    if request.method == "POST":

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:
                login(request, user)
                return redirect("portfolio")

    else:
        form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("portfolio")


def register_view(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            
            grupo = Group.objects.get(name='autores')
            user.groups.add(grupo)
            

            login(request, user)

            return redirect("portfolio")

    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


