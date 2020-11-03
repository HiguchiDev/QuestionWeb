from django.contrib import admin
from question.models import Category, Question, TextChoice, QuestionDispType
# Register your models here.

admin.site.register(Category)
admin.site.register(Question)
admin.site.register(TextChoice)
admin.site.register(QuestionDispType)