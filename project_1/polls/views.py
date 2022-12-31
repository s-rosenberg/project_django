from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.utils import timezone
from django.urls import reverse
from django.views import generic
from django.db.models.query import QuerySet
from .models import Question, Choice

##################### VIEWS DEFINIDOS COMO FUNCIONES ##############################

def index_old(request) -> HttpResponse:
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([question.question_text for question in latest_question_list])
    return HttpResponse(output)

def index_without_render(request) -> HttpResponse:
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def index(request) -> HttpResponse:
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, template_name='polls/index.html', context=context)

def detail_old(request, question_id:int) -> HttpResponse:
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404('Question does not exist')

    return render(request, template_name='polls/detail.html', context={'question':question})

def detail(request, question_id:int) -> HttpResponse:
    question = get_object_or_404(Question, pk=question_id)
    return render(request, template_name='polls/detail.html', context={'question': question})

def results(request, question_id:int) -> HttpResponse:
    question = get_object_or_404(Question, pk=question_id)
    return render(request, template_name='polls/results.html', context= {'question': question}) 

##################### VIEWS DEFINIDOS COMO CLASES ##############################
############################# GENERICAS ########################################

def get_queryset_older_than_now() -> QuerySet[Question]:
    return Question.objects.filter(pub_date__lte=timezone.now())

def get_questions_with_choices(query_set:QuerySet[Question]):
    return [question for question in query_set if question.choice_set.all()]

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        query_set = get_queryset_older_than_now().order_by('-pub_date')[:5]
        return get_questions_with_choices(query_set)

# las vistas genericas necesitan saber sobre que modelo actuaran (para eso se usa el attr model)
# DetailView espera que la primary key este en la URL -> por eso se cambia de question_id a pk en polls/urls.py
# se crea el attr template_name ya que por default es <app name>/<model name>_detail.html
# generic views doc: https://docs.djangoproject.com/en/4.1/topics/class-based-views/

# TODO evitar detail y results para question que no tengan choices

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excluye Question no publicada aun
        """
        return get_queryset_older_than_now()
        
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        """
        Excluye Question no publicada aun
        """
        return get_queryset_older_than_now()

def vote(request, question_id:int) -> HttpResponse:
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        context = {
            'question':question,
            'error_message': "You didn't select a choice"
        }
        return render(request, template_name= 'polls/detail.html', context=context)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
        # This function helps avoid having to hardcode a URL in the view function. 
        # It is given the name of the view that we want to pass control to and 
        # the variable portion of the URL pattern that points to that view