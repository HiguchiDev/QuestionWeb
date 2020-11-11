# Generated by Django 3.1.2 on 2020-11-11 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0021_category_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagequestion',
            name='choice_type',
            field=models.CharField(default='img', max_length=1024, verbose_name='選択肢のタイプ'),
        ),
        migrations.AddField(
            model_name='question',
            name='choice_type',
            field=models.CharField(default='text', max_length=1024, verbose_name='選択肢のタイプ'),
        ),
    ]
