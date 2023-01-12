from django.urls import path

from . import views

app_name = 'passwords'
urlpatterns = [
    # path('new_password/', views.new_password, name='new_password'),
    path('save_password/', views.save_password, name='save_password')
]