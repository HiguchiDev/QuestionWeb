# Generated by Django 3.1.2 on 2020-11-03 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0007_question_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='DispType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, verbose_name='表示形式名')),
            ],
        ),
        migrations.RemoveField(
            model_name='question',
            name='comment',
        ),
        migrations.AddField(
            model_name='question',
            name='ng_comment',
            field=models.CharField(default='', max_length=1024, verbose_name='解説（正解の場合）'),
        ),
        migrations.AddField(
            model_name='question',
            name='ok_comment',
            field=models.CharField(default='', max_length=1024, verbose_name='解説（正解の場合）'),
        ),
    ]