# Generated by Django 4.2.7 on 2023-11-22 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disciplinetracking', '0008_alter_violation_pictures'),
    ]

    operations = [
        migrations.AddField(
            model_name='violation',
            name='action_taken',
            field=models.TextField(blank=True, choices=[('Action Taken', 'Action Taken'), ('Action Not Taken', 'Action Not Taken')], default='Action Not Taken', null=True),
        ),
        migrations.AddField(
            model_name='violation',
            name='intervention_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='violation',
            name='recommendation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='violation',
            name='pictures',
            field=models.ImageField(blank=True, null=True, upload_to='violations'),
        ),
        migrations.AlterField(
            model_name='violation',
            name='school_year',
            field=models.CharField(choices=[('SY2022-2023', 'SY2022-2023'), ('SY2023-2024', 'SY2023-2024')], default='2023-2024', max_length=100),
        ),
    ]
