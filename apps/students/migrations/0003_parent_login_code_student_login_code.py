# Generated by Django 5.2 on 2025-04-24 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_lesson_end_time_alter_lesson_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='parent',
            name='login_code',
            field=models.CharField(blank=True, max_length=14, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='student',
            name='login_code',
            field=models.CharField(blank=True, max_length=14, null=True, unique=True),
        ),
    ]
