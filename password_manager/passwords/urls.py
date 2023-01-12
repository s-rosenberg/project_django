from django.urls import path

from . import views

app_name = 'passwords'
urlpatterns = [
    path('save_password/', views.save_password, name='save_password')
]