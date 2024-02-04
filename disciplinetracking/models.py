from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
# from .summary_utils import update_summary

SchoolYear_Choices = (
    ('2022-2023','SY2022-2023'),
    ('2023-2024','SY2023-2024'),
    ('2024-2025','SY2024-2025'),
    ('2025-2026','SY2025-2026'),
    ('2026-2027','SY2026-2027'),
    ('2027-2028','SY2027-2028'),
    
)

action_taken = (
    ('Meeting with the adviser','Meeting with the adviser'),
    ('Call the attention of parents','Call the attention of parents'),
    ('Give extracurricular activities','Give extracurricular activities'),
    ('Endorse to Child Protection Office','Endorse to Child Protection Office'),
    ('Endorse to Brgy. Child Protection Council','Endorse to Brgy. Child Protection Council'),
    ('Reprimand','Reprimand'),
)

Offense_Choices = (
        ('Offense1', 'Constant loitering in the school perimeters'),
        ('Offense2', 'Vandalism and deliberately causing damage to school properties'),
        ('Offense3', 'Constant used of unauthorized electrical outlets for personal used'),
        ('Offense4', 'Constant used of cellphones during classes hours'),
        ('Offense5', 'Constant misbehaving activities that cause disruption'),
        ('Offense6', 'Bullying'),
        ('Offense7', 'Threats'),
        ('Offense8', 'Physical injury'),
        ('Offense9', 'Cheating'),
        ('Offense10', 'Falsifying school and teachers documents'),
        ('Offense11', 'Constant absences'),
        ('Offense12', 'Cutting of classes'),
        ('Offense13', 'Falsifying school and teachers documents'),
        ('Offense14', 'Fighting on campus and off campus'),
        ('Offense15', 'Position of deadly weapon'),
        ('Offense16', 'Smoking inside the campus'),
        ('Offense17', 'Drug Related issues'),
        ('Offense18', 'Gambling'),
        ('Offense19', 'Stealing'),
        ('Offense20', 'Position/ drinking of alcoholic beverages'),
        ('Offense21', 'Sexual harassments'),
        ('Others', 'Others')
    )

class Student(models.Model):
    lrn = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    birthday = models.DateField(blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('disciplinetracking-list', kwargs={'pk':self.pk})

class Violation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    violation_number = models.PositiveIntegerField(null=True, blank=True,default=1)
    selected_offense = models.CharField(max_length=300, choices=Offense_Choices, default='Offense1')
    custom_description = models.CharField(max_length=300, blank=True, null=True)
    narrative_report = models.CharField(max_length=300)
    school_year = models.CharField(max_length=15, choices=SchoolYear_Choices, default='2023-2024')
    pictures = models.ImageField(upload_to='violations', null=True,blank=True)
    date_committed = models.DateTimeField(default=timezone.now,null=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT)
    intervention_date = models.DateTimeField(null=True, blank=True)
    action_taken = models.TextField(max_length=100,choices=action_taken, default="Meeting with the adviser")
    recommendation = models.CharField(max_length=300,null=True, blank=True)

    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_summary()
    
    def delete(self, *args, **kwargs):
        offense_type = self.get_selected_offense_display() if self.get_selected_offense_display() != 'Others' else self.custom_description
        summary = OffenseSummary.objects.filter(
            school_year=self.school_year,
            offense_type=offense_type
        ).first()

        if summary and summary.count > 0:
            summary.count -= 1
            summary.save()

        super().delete(*args, **kwargs)

    def update_summary(self):
        offense_type = self.get_selected_offense_display() if self.get_selected_offense_display() != 'Others' else self.custom_description
        summary, created = OffenseSummary.objects.get_or_create(
            school_year=self.school_year,
            offense_type=offense_type,
            count = 1
        )

        if not created:
            summary.count += 1
            summary.save()
        


    def __str__(self):
        return f"Violation for {self.student.name}"

    def get_absolute_url(self):
        return reverse('disciplinetracking-list', kwargs={'pk':self.student.pk})

    @property
    def image_url(self):
        if self.image:
            return getattr(self.photo, 'url', None)
        return None
    
class OffenseSummary(models.Model):
    school_year = models.CharField(max_length=15)
    offense_type = models.CharField(max_length=300)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.school_year} - {self.offense_type} ({self.count} offenses)"

# @receiver(post_save, sender=Violation)
# def update_summary_on_save(sender, instance, **kwargs):
#     instance.update_summary()


# @receiver(post_delete, sender=Violation)
# def update_summary_on_delete(sender, instance, **kwargs):
#     offense_type = instance.get_selected_offense_display() if instance.get_selected_offense_display() != 'Others' else instance.custom_description
#     summary = OffenseSummary.objects.filter(
#         school_year=instance.school_year,
#         offense_type=offense_type
#     ).first()

#     if summary and summary.count > 0:
#         summary.count -= 1
#         summary.save()