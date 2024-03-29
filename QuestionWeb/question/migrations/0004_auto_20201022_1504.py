# Generated by Django 3.1.2 on 2020-10-22 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0003_question_answer_choice_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='category_no',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='カテゴリNo.'),
        ),
        migrations.AlterField(
            model_name='textchoice',
            name='choice_no',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='選択肢No.'),
        ),
    ]
