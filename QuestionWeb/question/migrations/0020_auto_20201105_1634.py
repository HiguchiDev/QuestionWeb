# Generated by Django 3.1.2 on 2020-11-05 07:34

from django.db import migrations, models
import django.db.models.deletion
import question.models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0019_imagequestion_wrap_back_num'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, verbose_name='グループ名称')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='CategoryGroup',
            field=models.ForeignKey(default=question.models.set_default_cateory_group, on_delete=django.db.models.deletion.CASCADE, to='question.categorygroup'),
        ),
    ]
