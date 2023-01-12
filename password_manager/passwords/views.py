from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from .forms import PasswordForm
from .models import SavedPassword, Site

def save_password(request:HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            password = form.cleaned_data['password']
            site_name = form.cleaned_data['site']
            site_url = form.cleaned_data['site_url']
            site = Site(site_name=site_name, site_url=site_url)
            saved_password = SavedPassword(
                username=user, 
                password=password,
                site=site
                )
            site.save()
            saved_password.save()
            return HttpResponse('PIOLA')
    else: 
        form = PasswordForm()
    return render(request, 'passwords/save_password.html', {'form':form})

# def new_password(request):
#     form = PasswordForm()
#     return render(request, template_name='passwords/save_password.html')