from django.db import models

class Category(models.Model):
    name = models.CharField('カテゴリ名称', max_length=512, blank=False)
    category_no = models.PositiveSmallIntegerField(verbose_name='カテゴリNo.', default=1)

    def __str__(self):
        return self.name

def set_default_disp_type():
    disp_type, _ = QuestionDispType.objects.get_or_create(name='左寄せ')
    return disp_type.id

class QuestionDispType(models.Model):
    name = models.CharField('表示形式名', max_length=512, blank=False)

    def __str__(self):
        return self.name


# Create your models here.
class Question(models.Model):
    body = models.CharField('本文（漢字）', max_length=1024)
    body_kana = models.CharField('本文（ひらがな）', max_length=1024, default="")
    Category = models.ManyToManyField(Category)
    question_no = models.PositiveSmallIntegerField(verbose_name='問題No.', default=0)
    answer_choice_no = models.PositiveSmallIntegerField(verbose_name='正解No.', default=1)
    ok_comment = models.CharField('解説（正解の場合）', max_length=1024, default="")
    ng_comment = models.CharField('解説（不正解の場合）', max_length=1024, default="")
    question_disp_type = models.ForeignKey(QuestionDispType, on_delete=models.SET_DEFAULT, default=set_default_disp_type)

    def __str__(self):
        return self.body

class TextChoice(models.Model):
    body = models.CharField('選択肢（漢字）', max_length=512)
    body_kana = models.CharField('選択肢（ひらがな）', max_length=1024, default="")
    Question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_no = models.PositiveSmallIntegerField(verbose_name='選択肢No.', default=1)

    def __str__(self):
        return self.body
