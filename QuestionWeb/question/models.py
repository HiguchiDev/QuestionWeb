from django.db import models

class Category(models.Model):
    name = models.CharField('カテゴリ名称', max_length=512, blank=False)
    category_no = models.PositiveSmallIntegerField(verbose_name='カテゴリNo.', default=1)

    def __str__(self):
        return self.name

# Create your models here.
class Question(models.Model):
    body = models.CharField('本文（漢字）', max_length=1024)
    body_kana = models.CharField('本文（ひらがな）', max_length=1024, default="")
    Category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    question_no = models.PositiveSmallIntegerField(verbose_name='問題No.', default=0)
    answer_choice_no = models.PositiveSmallIntegerField(verbose_name='正解No.', default=1)

    def __str__(self):
        return self.body

class TextChoice(models.Model):
    body = models.CharField('選択肢（漢字）', max_length=512)
    body_kana = models.CharField('選択肢（ひらがな）', max_length=1024, default="")
    Question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_no = models.PositiveSmallIntegerField(verbose_name='選択肢No.', default=1)

    def __str__(self):
        return self.body
