# Generated by Django 4.2.7 on 2023-11-22 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disciplinetracking', '0009_violation_action_taken_violation_intervention_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='violation',
            name='pictures',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='violations'),
        ),
    ]
