# Generated by Django 2.0.3 on 2018-05-24 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_auto_20180524_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='password',
            field=models.CharField(max_length=20, verbose_name='密码'),
        ),
    ]
