# Generated by Django 4.2.7 on 2023-11-22 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disciplinetracking', '0011_alter_violation_pictures'),
    ]

    operations = [
        migrations.AlterField(
            model_name='violation',
            name='intervention_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]