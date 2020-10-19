from django.contrib import admin
from question.models import Category, Question, TextChoice
# Register your models here.

admin.site.register(Category)
admin.site.register(Question)
admin.site.register(TextChoice)