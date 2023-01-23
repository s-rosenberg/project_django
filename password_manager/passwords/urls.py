from django.urls import path, include

from . import views

app_name = 'passwords'
urlpatterns = [
    path('save_password/', views.save_password, name='save_password'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register_user, name='register')
]