# Generated by Django 5.0.3 on 2024-04-01 19:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authen', '0005_alter_studentextended_standard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foundationalmodel',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='foundationalmodel',
            name='name',
            field=models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(limit_value=5, message='Please enter name of good length.')], verbose_name='Name'),
        ),
    ]
