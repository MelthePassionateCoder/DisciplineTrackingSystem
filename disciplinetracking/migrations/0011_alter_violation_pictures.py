# Generated by Django 4.2.7 on 2023-11-22 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disciplinetracking', '0010_alter_violation_pictures'),
    ]

    operations = [
        migrations.AlterField(
            model_name='violation',
            name='pictures',
            field=models.ImageField(blank=True, null=True, upload_to='violations'),
        ),
    ]
