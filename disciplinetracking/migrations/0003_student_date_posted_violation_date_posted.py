# Generated by Django 4.2.7 on 2023-11-19 18:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('disciplinetracking', '0002_alter_student_created_by_violation'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='date_posted',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
        migrations.AddField(
            model_name='violation',
            name='date_posted',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
    ]