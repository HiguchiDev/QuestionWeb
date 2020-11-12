from django.shortcuts import render
from django.views.generic import TemplateView
from question.models import Question, TextChoice, Category, ImageQuestion, CategoryGroup
import random
from django.http import HttpResponseRedirect
from django.shortcuts import reverse

# Create your views here.

QUESTION_MAX_QTY = 5

class TopPageView(TemplateView):
    template_name = "top.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        sample_category = CategoryGroup.objects.get(name="サンプル問題").category_set.all().first() #サンプル問題カテゴリのみのはず。
        rand_int = random.randint(0, 1)

        # text優先
        if rand_int == 0:
            if sample_category.question_set.all().count() > 0:
                question_rand_int = rand_int = random.randint(0, sample_category.question_set.all().count() - 1)
                ctx['sample_question'] = sample_category.question_set.all()[question_rand_int]
                
            elif sample_category.imagequestion_set.all().count() > 0:
                question_rand_int = rand_int = random.randint(0, sample_category.imagequestion_set.all().count() - 1)
                ctx['sample_question'] = sample_category.imagequestion_set.all()[question_rand_int]

        #image優先
        elif rand_int == 1:
            if sample_category.imagequestion_set.all().count() > 0:
                question_rand_int = rand_int = random.randint(0, sample_category.imagequestion_set.all().count() - 1)
                ctx['sample_question'] = sample_category.imagequestion_set.all()[question_rand_int]
            elif sample_category.question_set.all().count() > 0:
                question_rand_int = rand_int = random.randint(0, sample_category.question_set.all().count() - 1)
                ctx['sample_question'] = sample_category.question_set.all()[question_rand_int]

        princess_group = CategoryGroup.objects.get(name="プリンセス別")
        ctx['princess_category_list'] = princess_group.category_set.all().order_by('category_no')

        difficulty_group = CategoryGroup.objects.get(name="難易度別")
        ctx['difficulty_category_list'] = difficulty_group.category_set.all().order_by('category_no')

        field_group = CategoryGroup.objects.get(name="分野別")
        ctx['field_category_list'] = field_group.category_set.all().order_by('category_no')

        return ctx


class QuestionView(TemplateView):
    template_name = "question_main.html"

    def get(self, request, **kwargs):
        
        question_no = kwargs.get('question_no')
        category_id = kwargs.get('category_id')

        question_qty = Category.objects.get(pk=category_id).question_set.all().count()
        question_qty += Category.objects.get(pk=category_id).imagequestion_set.all().count()

        if question_qty < QUESTION_MAX_QTY:
            return HttpResponseRedirect(reverse('preparation'))

        # セッション切れチェック
        if question_no == 1 and self.request.session.get('is_question_end', False) == False:
            self.request.session.clear() # 上限前に別カテゴリの問題に挑戦した場合はクリア

        elif question_no != 1 and not self.request.session.get('question_id_list', False):
            return HttpResponseRedirect(reverse('session_expire'))

        elif self.request.session.get('is_question_end', False):
            return HttpResponseRedirect(reverse('stop'))

        return super().get(request, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        random_question_id_list = []
        category = Category.objects.get(pk=self.kwargs.get('category_id'))

        if not self.request.session.get('question_id_list', False):
            for q in category.question_set.all():
                random_question_id_list.append({'text' : q.id})
            
            for q in category.imagequestion_set.all():
                random_question_id_list.append({'img' : q.id})

            random.shuffle(random_question_id_list)
            
            self.request.session['question_id_list'] = random_question_id_list
            
        
        question_id_list = self.request.session.get('question_id_list')
        q_no = self.kwargs.get('question_no')

        rem_question_id_list = question_id_list[(q_no-1):]

        question_list = []

        for q_id_dic in rem_question_id_list:
            if 'text' in q_id_dic:
                question_list.append(Question.objects.get(pk=q_id_dic['text']))
            elif 'img' in q_id_dic:
                question_list.append(ImageQuestion.objects.get(pk=q_id_dic['img']))

        ctx['category'] = category

        ctx['question_list'] = question_list
        ctx['rem_res_cnt'] = QUESTION_MAX_QTY - self.request.session.get('res_cnt', 0)
        ctx['res_cnt'] = self.request.session.get('res_cnt', 0)

        return ctx

    def __get_text_question_id(self, random_question_id_list, category):
        question_list = category.question_set.all()

        for i in range(question_list.count()):
            rand_int = random.randint(0, question_list.count() - 1)
            rand_question = question_list[rand_int]

            if self.__is_selected(random_question_id_list, 'text', rand_question) == False:
                return rand_question.id
        
        return None

    def __get_img_question_id(self, random_question_id_list, category):
        question_list = category.imagequestion_set.all()

        for i in range(question_list.count()):
            rand_int = random.randint(0, question_list.count() - 1)
            rand_question = question_list[rand_int]

            if self.__is_selected(random_question_id_list, 'img', rand_question) == False:
                return rand_question.id
        
        return None

    
    def __is_selected(self, random_question_id_list, key, question):
        
        for rand_question_id_dict in random_question_id_list:
            if rand_question_id_dict.get(key) == question.id:
                return True

        return False

class QuestionStopView(TemplateView):
    template_name = "question_stop.html"

class CategoryView(TemplateView):
    template_name = "category.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        
        category_list = Category.objects.all()

        ctx['category_list'] = category_list

        return ctx

class AnswerResultView(TemplateView):
    template_name = "question_comment.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        
        if self.kwargs.get('question_type') == 'text':
            question = Question.objects.get(pk=self.kwargs.get('question_id'))
        elif self.kwargs.get('question_type') == 'img':
            question = ImageQuestion.objects.get(pk=self.kwargs.get('question_id'))

        answer_choice_no = question.answer_choice_no

        ctx['answer_choice_no'] = answer_choice_no
        ctx['choice_no'] = self.kwargs.get('choice_no')
        ctx['question'] = question
        ctx['category_id'] = self.kwargs.get('category_id')

        res_cnt = self.request.session.get('res_cnt', 0)
        res_cnt += 1
        self.request.session['res_cnt'] = res_cnt

        if res_cnt >= QUESTION_MAX_QTY:
            self.request.session['is_question_end'] = True

        return ctx

class SessionExpireView(TemplateView):
    template_name = "session_expire.html"

class PreparationView(TemplateView):
    template_name = "question_preparation.html"

class SampleAnswerView(TemplateView):
    template_name = "sample_answer.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        
        if self.kwargs.get('question_type') == 'text':
            question = Question.objects.get(pk=self.kwargs.get('question_id'))
        elif self.kwargs.get('question_type') == 'img':
            question = ImageQuestion.objects.get(pk=self.kwargs.get('question_id'))

        ctx['princess_category'] = Category.objects.get(name="シンデレラ")
        ctx['question'] = question

        return ctx


class SandView(TemplateView):
    template_name = "sand.html"