import datetime
from django.db import models
from django.contrib import admin

from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
    def __str__(self) -> str:
        return self.question_text

    @admin.display(
        boolean = True,
        ordering = 'pub_date',
        description = 'Published recently?'
    ) # poniendo mas lindo como se displayea en el admin page
    def was_published_recently(self) -> bool:
        now = timezone.now()
        return now >= self.pub_date >= now - datetime.timedelta(days=1)

# EXPLICACION DE RELACION ENTRE QUESTION & CHOICE
# Give the Question a couple of Choices. The create call constructs a new
# Choice object, does the INSERT statement, adds the choice to the set
# of available choices and returns the new Choice object. Django creates
# a set to hold the "other side" of a ForeignKey relation
# (e.g. a question's choice) which can be accessed via the API.
# para acceder a ese choice_set: question.choice_set.all()

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.choice_text