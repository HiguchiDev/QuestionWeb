from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView, DeleteView
from extra_views import CreateWithInlinesView, InlineFormSetFactory, UpdateWithInlinesView
from extra_views.generic import GenericInlineFormSetView
from question.models import Question, TextChoice, Category, ImageQuestion, ImageChoice
from django.urls import reverse
from django.forms import ModelForm, inlineformset_factory, Textarea
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.shortcuts import redirect


class LoginRequiredMixin(object):
    @method_decorator(login_required(login_url = '/accounts/login/')) #ここがかわった
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class CategoryQuestionList(LoginRequiredMixin, ListView):
    model = Question
    template_name = "question/category_question_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(pk=self.kwargs.get('category_id'))

        context['category'] = category
        context['img_question_list'] = category.imagequestion_set.all()

        return context

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        category = Category.objects.get(pk=category_id)
        
        return category.question_set.all()

# Create your views here.
class QuestionList(LoginRequiredMixin, ListView):
    model = Question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['img_question_list'] = ImageQuestion.objects.all()

        return context


# Create your views here.
class CategoryList(LoginRequiredMixin, ListView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context



class QuestionDetail(LoginRequiredMixin, DetailView):
    model = Question
    #queryset = Question.objects.select_related('Category', 'TextChoice').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = context.get("object")
        choices = question.textchoice_set.all().order_by("choice_no")
        context["choices"] = choices
        context["category_id"] = self.kwargs.get('category_id')
        
        if self.kwargs.get('category_id'):
            context["category_name"] = Category.objects.get(pk=self.kwargs.get('category_id')).name
        
        return context

class ImageQuestionDetail(LoginRequiredMixin, DetailView):
    model = ImageQuestion
    #queryset = Question.objects.select_related('Category', 'TextChoice').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = context.get("object")
        choices = question.imagechoice_set.all().order_by("choice_no")
        context["choices"] = choices
        context["category_id"] = self.kwargs.get('category_id')
        
        if self.kwargs.get('category_id'):
            context["category_name"] = Category.objects.get(pk=self.kwargs.get('category_id')).name
        
        return context

class TextChoiceForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(TextChoiceForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = TextChoice
        fields = ("choice_no", "body", "body_kana")
        widgets = {
            'body': Textarea(attrs={'rows':2, 'cols':1}),
            'body_kana': Textarea(attrs={'rows':2, 'cols':1}),
        }


class ImageChoiceForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ImageChoiceForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = ImageChoice
        fields = ("choice_no", "img")
        
        

class TextChoiceInlineFormSetForCreate(InlineFormSetFactory):

    model = TextChoice
    form_class = TextChoiceForm
    #initial = [{'name': 'example1'}, {'name', 'example2'}]
    #prefix = 'item-form'
    factory_kwargs = {'extra': 2, 'max_num': None,
                      'can_order': False, 'can_delete': True}
    #formset_kwargs = {'auto_id': 'my_id_%s'}


class ImageChoiceInlineFormSetForCreate(InlineFormSetFactory):

    model = ImageChoice
    form_class = ImageChoiceForm
    #initial = [{'name': 'example1'}, {'name', 'example2'}]
    #prefix = 'item-form'
    factory_kwargs = {'extra': 2, 'max_num': None,
                      'can_order': False, 'can_delete': True}
    #formset_kwargs = {'auto_id': 'my_id_%s'}


class TextChoiceInlineFormSetForUpdate(InlineFormSetFactory):

    model = TextChoice
    form_class = TextChoiceForm
    factory_kwargs = {'extra': 0, 'max_num': None,
                      'can_order': False, 'can_delete': True}

class ImageChoiceInlineFormSetForUpdate(InlineFormSetFactory):

    model = ImageChoice
    form_class = ImageChoiceForm
    factory_kwargs = {'extra': 0, 'max_num': None,
                      'can_order': False, 'can_delete': True}


class QuestionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Question
        fields = ['body', "body_kana", 'Category', 'answer_choice_no', 'ok_comment', 'ng_comment', 'question_disp_type',]

        widgets = {
            'body': Textarea(attrs={'rows':2, 'cols':1}),
            'body_kana': Textarea(attrs={'rows':2, 'cols':1}),
            'ok_comment': Textarea(attrs={'rows':2, 'cols':1}),
            'ng_comment': Textarea(attrs={'rows':2, 'cols':1}),
        }

class ImageQuestionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ImageQuestionForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = ImageQuestion
        fields = ['body', "body_kana", 'Category', 'answer_choice_no', 'ok_comment', 'ng_comment',]

        widgets = {
            'body': Textarea(attrs={'rows':2, 'cols':1}),
            'body_kana': Textarea(attrs={'rows':2, 'cols':1}),
            'ok_comment': Textarea(attrs={'rows':2, 'cols':1}),
            'ng_comment': Textarea(attrs={'rows':2, 'cols':1}),
        }



class QuestionCreateFormsetView(LoginRequiredMixin, CreateWithInlinesView):
    model = Question
    #fields = ("body", "category", )  # self.model の fields
    form_class = QuestionForm

    inlines = [TextChoiceInlineFormSetForCreate, ]
    template_name = "question/question_create_form.html"

    def get_success_url(self):
        return reverse('question_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_id'] = self.kwargs.get('category_id')
        
        return context

class ImageQuestionCreateFormsetView(LoginRequiredMixin, CreateWithInlinesView):
    model = ImageQuestion
    form_class = ImageQuestionForm

    inlines = [ImageChoiceInlineFormSetForCreate, ]
    template_name = "question/question_create_form_img.html"

    def get_success_url(self):
        return reverse('question_detail_img', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_id'] = self.kwargs.get('category_id')
        
        return context


class QuestionUpdateFormsetView(LoginRequiredMixin, UpdateWithInlinesView):
    model = Question
    #fields = ("body", "category", )  # self.model の fields
    form_class = QuestionForm

    inlines = [TextChoiceInlineFormSetForUpdate, ]
    template_name = "question/question_form.html"

    def get_success_url(self):
        return reverse('question_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_id'] = self.kwargs.get('category_id')
        
        return context

class ImageQuestionUpdateFormsetView(LoginRequiredMixin, UpdateWithInlinesView):
    model = ImageQuestion
    #fields = ("body", "category", )  # self.model の fields
    form_class = ImageQuestionForm

    inlines = [ImageChoiceInlineFormSetForUpdate, ]
    template_name = "question/question_form_img.html"

    def get_success_url(self):
        return reverse('question_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_id'] = self.kwargs.get('category_id')
        
        return context


class QuestionDeleteView(DeleteView):
    template_name = 'question/question_delete.html'
    model = Question

    def get_success_url(self):
        return reverse('question_list')

class ImageQuestionDeleteView(DeleteView):
    template_name = 'question/imagequestion_delete.html'
    model = ImageQuestion

    def get_success_url(self):
        return reverse('question_list')


class QuestionAddView(TemplateView):
    template_name = 'question/question_add.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(pk=self.kwargs.get('category_id'))
        category_question_id_list = category.question_set.values_list('id', flat=True)
        category_imagequestion_id_list = category.imagequestion_set.values_list('id', flat=True)
        not_exists_question_list = []
        not_exists_imgquestion_list = []

        all_question = Question.objects.all()
        all_imgquestion = ImageQuestion.objects.all()

        for question in all_question:
            if question.id not in category_question_id_list:
                not_exists_question_list.append(question)

        for question in all_imgquestion:
            if question.id not in category_imagequestion_id_list:
                not_exists_imgquestion_list.append(question)

        context['category'] = category
        context['question_list'] = not_exists_question_list
        context['img_question_list'] = not_exists_imgquestion_list
        context['add_result'] = self.kwargs.get('add_result')

        return context

    def post(self, request, *args, **kwargs):
        category = Category.objects.get(pk=request.POST['category_id'])

        if request.POST.get('question_id') is not None:
            question = Question.objects.get(pk=request.POST['question_id'])
            question.Category.add(category)
        elif request.POST.get('imagequestion_id') is not None:
            question = ImageQuestion.objects.get(pk=request.POST['imagequestion_id'])
            question.Category.add(category)

        return redirect('/edit/question/add/' + request.POST['category_id'] + '/success')
 
 
class QuestionExclusionView(TemplateView):
    template_name = 'question/question_exclusion.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(pk=self.kwargs.get('category_id'))

        context['category'] = category
        context['question_list'] = category.question_set.all()
        context['imagequestion_list'] = category.imagequestion_set.all()
        context['exclusion_result'] = self.kwargs.get('exclusion_result')

        return context

    def post(self, request, *args, **kwargs):
        
        category = Category.objects.get(pk=request.POST['category_id'])

        if request.POST.get('question_id') is not None:
            question = Question.objects.get(pk=request.POST['question_id'])
            question.Category.remove(category)
        elif request.POST.get('imagequestion_id') is not None:
            question = ImageQuestion.objects.get(pk=request.POST['imagequestion_id'])
            question.Category.remove(category)

        return redirect('/edit/question/exclusion/' + request.POST['category_id'] + '/success')