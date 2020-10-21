from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from extra_views import CreateWithInlinesView, InlineFormSetFactory, UpdateWithInlinesView
from extra_views.generic import GenericInlineFormSetView
from question.models import Question, TextChoice, Category
from django.urls import reverse
from django.forms import ModelForm, inlineformset_factory, Textarea


# Create your views here.
class QuestionList(ListView):
    model = Question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_id'] = self.kwargs.get('category_id')

        return context

    def get_queryset(self):
        categori_id = self.kwargs.get('category_id')
        return self.model.objects.filter(Category_id=categori_id).order_by('question_no')

# Create your views here.
class CategoryList(ListView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

class QuestionDetail(DetailView):
    model = Question
    #queryset = Question.objects.select_related('Category', 'TextChoice').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = context.get("object")
        choices = question.textchoice_set.all().order_by("choice_no")
        context["choices"] = choices
        
        return context


class TextChoiceForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(TextChoiceForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = TextChoice
        fields = ("choice_no", "body")
        widgets = {
            'body': Textarea(attrs={'rows':2, 'cols':1}),
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


class CategoryForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Category
        fields = ['name']

class QuestionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Question
        fields = ['body', 'Category']

        widgets = {
            'body': Textarea(attrs={'rows':5, 'cols':1}),
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



class QuestionSortOrDeleteFormSetView(UpdateWithInlinesView):
    model = Category
    
    form_class = CategoryForm
    inlines = [QuestionInlineFormSet, ]
    template_name = "question/question_sort.html"

    def get_success_url(self):
        return reverse('question_list', kwargs={'category_id': self.object.pk})


class QuestionCreateFormsetView(CreateWithInlinesView):
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

class QuestionUpdateFormsetView(UpdateWithInlinesView):
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
