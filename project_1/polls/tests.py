from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from typing import List
from .models import Question
import datetime


class QuestionModelTests(TestCase):
        
    def test_was_published_recently_with_future_questions(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
    
    def test_was_publiched_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day
        """
        time = timezone.now() + datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)
    
    def test_was_publiched_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day
        """
        time = timezone.now() + datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), False)

# test views
def create_question(question_text: str, days: int) -> Question:
    """
    Crear Question con un question_text publicado para un numero determinado de dias
    como offset desde hoy (positivo para el futuro y negativo para el pasado)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

def create_question_with_choices(question_text:str, days: int) -> Question:
    question = create_question(question_text=question_text, days=days)
    create_choices(question)
    return question

def create_choices(question:Question):
    """
    Crear choices para una question en especifico
    """
    question.choice_set.create(choice_text='Choice 1', votes=0)
    question.choice_set.create(choice_text='Choice 2', votes=0)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        Si no hay Questions, debe mostrar el mensaje apropiado
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])
    
    def test_past_question(self):
        """
        Questions con pub_date pasadas deben estar en la index page
        """
        question = create_question_with_choices(question_text='Past question.', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )
    
    def test_future_question(self):
        """
        Questions con pub_date en el futuro no deben estar en la index page
        """
        create_question_with_choices(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [],
        )
    
    def test_future_and_past_questions(self):
        """
        Solo questions del pasado deben estar en la index page
        """
        past_question = create_question_with_choices(question_text='Past question.', days=-30)
        create_question_with_choices(question_text='Future question.', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [past_question],
        )

    def test_two_past_questions(self):
        """
        Solo questions del pasado deben estar en la index page
        """
        past_question_1 = create_question_with_choices(question_text='Past question 1.', days=-30)
        past_question_2 = create_question_with_choices(question_text='Past question 2.', days=-3)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [past_question_2, past_question_1],
        )

    def test_question_with_choices(self):
        """
        question con choices deben estar en la index page y debe mostrar su texto
        """
        question = create_question_with_choices(question_text='Question with choices.', days=-1)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question]
        )

    def test_question_with_no_choices(self):
        question = create_question(question_text='Question with no choices.', days=-1)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_question_with_and_withour_choices(self):
        question_with_choices = create_question_with_choices(question_text='Question with choices.', days=-1)
        question_without_choices = create_question(question_text='Question with no choices.', days=-1)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question_with_choices]
        )
def generic_future_question_test(test_case_class:TestCase, urlpattern:str) -> None:
    future_question = create_question(question_text='Future question.', days=2)
    url = reverse(urlpattern, args=(future_question.id,))
    response = test_case_class.client.get(url)
    test_case_class.assertEqual(response.status_code, 404)

def generic_past_question_test(test_case_class:TestCase, urlpattern:str) -> None:
    past_question = create_question(question_text='Past question.', days=-2)
    url = reverse(urlpattern, args=(past_question.id,))
    response = test_case_class.client.get(url)
    test_case_class.assertContains(response, past_question.question_text)

class QuestionDetailViewTests(TestCase):
    
    def test_future_question(self):
        """
        detail view para una future question debe devolver 404 Not Found
        """
        generic_future_question_test(self, 'polls:detail')
    

    def test_past_question(self):
        """
        detail view para past question debe devolver el texto de la question
        """
        generic_past_question_test(self, 'polls:detail')

class QuestionResultsViewTests(TestCase):

    def test_future_question(self):
        """
        results view no debe existir para una future question (debe devolver 404)
        """
        generic_past_question_test(self, 'polls:results')
    
    def test_past_question(self):
        """
        results view para past question debe incluir el texto de la question
        """
        generic_past_question_test(self, 'polls:results')

# TODO test case para question with no choices (estaria en el index view)
# TODO modificar tests para que creen las choices 
"""
Ejercicio:
We ought to add a similar get_queryset method to ResultsView and create a new test class for that view. 
It’ll be very similar to what we have just created; in fact there will be a lot of repetition.

We could also improve our application in other ways, adding tests along the way. For example, 
it’s silly that Questions can be published on the site that have no Choices. 
So, our views could check for this, and exclude such Questions. 
Our tests would create a Question without Choices and then test that it’s not published, 
as well as create a similar Question with Choices, and test that it is published.

Perhaps logged-in admin users should be allowed to see unpublished Questions, 
but not ordinary visitors. Again: 
whatever needs to be added to the software to accomplish this should be accompanied by a test, 
whether you write the test first and then make the code pass the test, 
or work out the logic in your code first and then write a test to prove it.
"""