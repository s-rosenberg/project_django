from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from .forms import PasswordForm

def save_password(request:HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            return HttpResponse('PIOLA')
    else: 
        form = PasswordForm()
    return render(request, 'passwords/save_password.html', {'form':form})

# def new_password(request):
#     form = PasswordForm()
#     return render(request, template_name='passwords/save_password.html')