# Generated by Django 3.1.7 on 2021-02-24 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_auto_20210224_0240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateField(verbose_name='due date'),
        ),
    ]
