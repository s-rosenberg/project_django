from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import render, get_object_or_404
from .models import Question

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
    return HttpResponse(f"You're looking at the results of question {question_id}")    

def vote(request, question_id:int) -> HttpResponse:
    return HttpResponse(f"You're voting on question {question_id}")    