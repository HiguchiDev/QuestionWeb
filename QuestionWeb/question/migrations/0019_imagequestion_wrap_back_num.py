# Generated by Django 3.1.2 on 2020-11-05 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0018_remove_question_avator'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagequestion',
            name='wrap_back_num',
            field=models.PositiveSmallIntegerField(default=3, verbose_name='1行の最大の選択肢数.'),
        ),
    ]