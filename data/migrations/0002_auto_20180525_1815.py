# Generated by Django 2.0.3 on 2018-05-25 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testcasescriptinfo',
            old_name='belong_module',
            new_name='belong_testcase',
        ),
    ]
