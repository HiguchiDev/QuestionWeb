# Generated by Django 3.1.2 on 2020-10-19 12:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, verbose_name='カテゴリ名称')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=1024, verbose_name='本文')),
                ('Category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='question.category')),
            ],
        ),
        migrations.CreateModel(
            name='TextChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=512, verbose_name='選択肢')),
                ('choice_no', models.PositiveSmallIntegerField(default=0, verbose_name='選択肢No.')),
                ('Question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.question')),
            ],
        ),
    ]
