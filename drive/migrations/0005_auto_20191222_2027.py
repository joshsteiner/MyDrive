# Generated by Django 3.0 on 2019-12-22 19:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drive', '0004_auto_20191222_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='name',
            field=models.CharField(max_length=256, validators=[django.core.validators.MinLengthValidator(1)]),
        ),
    ]