from django.shortcuts import render
from django.views.generic import TemplateView
from question.models import Question, TextChoice, Category
import random

# Create your views here.

class QuestionView(TemplateView):
    template_name = "question.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        

        random_question_id_list = []        
        category = Category.objects.get(pk=self.kwargs.get('category_id'))

        if not self.request.session.get('question_id_list', False):
            print('-------create session-----')
            question_list = category.question_set.all()

            while(len(random_question_id_list) < 5):
                rand_int = random.randint(0, question_list.count() - 1)
                rand_question = question_list[rand_int]

                if self.__is_selected(random_question_id_list, rand_question) == False:
                    random_question_id_list.append(rand_question.id)

            self.request.session.set_expiry(0)
            self.request.session['question_id_list'] = random_question_id_list
            
        
        question_id_list = self.request.session.get('question_id_list')

        question_id = question_id_list[self.kwargs.get('question_no') - 1]

        ctx['question'] = Question.objects.get(pk=question_id)
        ctx['category'] = category

        return ctx
    
    def __is_selected(self, random_question_id_list, question):
        
        for rand_question_id in random_question_id_list:
            if rand_question_id == question.id:
                return True

        return False

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
        
        question = Question.objects.get(pk=self.kwargs.get('question_id'))
        answer_choice_no = question.answer_choice_no

        ctx['answer_choice_no'] = answer_choice_no
        ctx['choice_no'] = self.kwargs.get('choice_no')
        ctx['question'] = question
        ctx['category_id'] = self.kwargs.get('category_id')

        return ctx