# Generated by Django 3.0.6 on 2020-07-30 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_rest_framework', '0006_auto_20200730_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blacklistedtoken',
            name='user',
            field=models.IntegerField(null=True),
        ),
    ]