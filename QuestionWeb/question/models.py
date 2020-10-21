from django.db import models

class Category(models.Model):
    name = models.CharField('カテゴリ名称', max_length=512, blank=False)

    def __str__(self):
        return self.name

# Create your models here.
class Question(models.Model):
    body = models.CharField('本文', max_length=1024)
    Category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    question_no = models.PositiveSmallIntegerField(verbose_name='問題No.', default=0)

    def __str__(self):
        return self.body

class TextChoice(models.Model):
    body = models.CharField('選択肢', max_length=512)
    Question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_no = models.PositiveSmallIntegerField(verbose_name='選択肢No.', default=0)

    def __str__(self):
        return self.body
