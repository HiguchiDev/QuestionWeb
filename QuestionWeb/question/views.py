from django.shortcuts import render
from django.views.generic import TemplateView
from question.models import Question, TextChoice, Category

# Create your views here.

class QuestionView(TemplateView):
    template_name = "question.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        
        category = Category.objects.get(pk=self.kwargs.get('category_id'))
        question = category.question_set.filter(question_no=self.kwargs.get('question_no'))

        ctx['question'] = question[0] # 基本一つしか取れないはず。
        ctx['choice_list'] = question[0].textchoice_set.all().order_by('choice_no')

        return ctx

class CategoryView(TemplateView):
    template_name = "category.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        
        category_list = Category.objects.all()

        ctx['category_list'] = category_list

        return ctx

class AnswerResultView(TemplateView):
    template_name = "answer.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        
        question_list = Question.objects.filter(Category_id=self.kwargs.get('category_id'),
                                                question_no=self.kwargs.get('question_no'))

        answer_choice_no = question_list[0].answer_choice_no

        ctx['answer_choice_no'] = answer_choice_no
        ctx['choice_no'] = self.kwargs.get('choice_no')
        ctx['question'] = question_list[0]

        return ctx