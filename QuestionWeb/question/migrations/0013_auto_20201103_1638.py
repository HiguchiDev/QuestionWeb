# Generated by Django 3.1.2 on 2020-11-03 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0012_auto_20201103_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='ng_comment',
            field=models.CharField(default='', max_length=1024, verbose_name='解説（不正解の場合）'),
        ),
    ]
