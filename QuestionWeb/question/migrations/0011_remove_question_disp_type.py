# Generated by Django 3.1.2 on 2020-11-03 07:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0010_questiondisptype'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='disp_type',
        ),
    ]
