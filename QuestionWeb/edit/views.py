from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from extra_views import CreateWithInlinesView, InlineFormSetFactory, UpdateWithInlinesView
from extra_views.generic import GenericInlineFormSetView
from question.models import Question, TextChoice, Category
from django.urls import reverse
from django.forms import ModelForm, inlineformset_factory, Textarea
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

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

        return context

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        category = Category.objects.get(pk=category_id)
        
        return category.question_set.all()

# Create your views here.
class QuestionList(LoginRequiredMixin, ListView):
    model = Question


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
            'body_kana': Textarea(attrs={'rows':5, 'cols':1}),
        }
        

class TextChoiceInlineFormSetForCreate(InlineFormSetFactory):

    model = TextChoice
    form_class = TextChoiceForm
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


class QuestionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Question
        fields = ['body', "body_kana", 'Category', 'answer_choice_no',]

        widgets = {
            'body': Textarea(attrs={'rows':5, 'cols':1}),
            'body_kana': Textarea(attrs={'rows':5, 'cols':1}),
        }


class QuestionCreateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(QuestionCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Question
        fields = ['body', 'body_kana', 'Category']

        widgets = {
            'body': Textarea(attrs={'rows':5, 'cols':1}),
            'body_kana': Textarea(attrs={'rows':5, 'cols':1}),
        }


class QuestionSortForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(QuestionSortForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Question
        fields = ['question_no', 'body',]

        widgets = {
            'body': Textarea(attrs={'rows':2, 'cols':1}),
        }


class QuestionInlineFormSet(InlineFormSetFactory):

    model = Question
    form_class = QuestionSortForm
    factory_kwargs = {'extra': 0, 'max_num': None,
                      'can_order': False, 'can_delete': True}


class QuestionCreateFormsetView(LoginRequiredMixin, CreateWithInlinesView):
    model = Question
    #fields = ("body", "category", )  # self.model の fields
    form_class = QuestionCreateForm

    inlines = [TextChoiceInlineFormSetForCreate, ]
    template_name = "question/question_create_form.html"

    def get_success_url(self):
        return reverse('question_detail', kwargs={'pk': self.object.pk})

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
