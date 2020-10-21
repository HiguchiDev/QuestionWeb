from django.shortcuts import render
from django.views.generic import TemplateView
from question.models import Question, TextChoice, Category

# Create your views here.

class QuestionView(TemplateView):
    template_name = "question.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        
        ctx['question'] = Question.objects.get(pk=self.kwargs.get('question_id'))

        return ctx