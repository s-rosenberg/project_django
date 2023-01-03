from django.contrib import admin
from .models import Question, Choice

# admin.site.register(Question)


class QuestionAdmin(admin.ModelAdmin):
    fileds = ['pub_date', 'question_text']
    # el orden de esta lista determinara el orden en el que aparecen en el admin form

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3
# si se prefiere que este mas compacto usar TabularInline
class ChoiceInlineTabular(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdminSeparator(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields':['question_text']}),
        ('Date Information', {
            'fields':
                ['pub_date'],
                'classes':['collapse']
                }
        )
    ]
    inlines = [ChoiceInlineTabular]
    # cada tupla del fieldset es (Nombre, fields_dict)
    list_display = ('question_text','pub_date','was_published_recently')
    # list_display son los campos del Model que se mostraran
    
admin.site.register(Question, QuestionAdminSeparator)

# # agregar Choices a Questions 
# admin.site.register(Choice)
# # esta manera no esta buena porque las tenes que agregar por separado de las questions


