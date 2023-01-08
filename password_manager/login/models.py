from django.db import models

class User(models.Model):
    username = models.CharField(max_length=40, unique=True)
    password = models.CharField(max_length=40)

    def __str__(self) -> str:
        return f'User({self.username})'