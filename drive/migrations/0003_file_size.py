# Generated by Django 3.0 on 2019-12-18 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drive', '0002_auto_20191213_2019'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='size',
            field=models.IntegerField(default=0),
        ),
    ]