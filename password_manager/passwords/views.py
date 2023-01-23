from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .forms import PasswordForm
from .models import SavedPassword, Site

def save_password(request:HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['user']
            password = form.cleaned_data['password']
            site_name = form.cleaned_data['site']
            site_url = form.cleaned_data['site_url']
            site = Site(site_name=site_name, site_url=site_url)
            if request.user.is_authenticated:
                logged_user = request.user
            saved_password = SavedPassword(
                username=username, 
                password=password,
                site=site,
                user=logged_user
                )
            site.save()
            saved_password.save()
            return HttpResponse('PIOLA')
    else: 
        form = PasswordForm()
    return render(request, 'passwords/save_password.html', {'form':form})

def register_user(request:HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('../accounts/login')
        else:
            form = UserCreationForm()
            context = {
                'error':'User already exists',
                'form':form
                }
            return render(request, template_name='registration/register.html', context=context)
    else:
        form = UserCreationForm()
        return render(request, 'registration/register.html', {'form':form})
# def new_password(request)
#     form = PasswordForm()
#     return render(request, template_name='passwords/save_password.html')