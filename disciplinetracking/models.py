from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

SchoolYear_Choices = (
    ('SY2022-2023','SY2022-2023'),
    ('SY2023-2024','SY2023-2024'),
)

action_taken = (
    ('Action Taken','Action Taken'),
    ('Action Not Taken','Action Not Taken'),
)

class Student(models.Model):
    lrn = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    birthday = models.DateField(blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now,null=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('disciplinetracking-list', kwargs={'pk':self.pk})

class Violation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    narrative_report = models.TextField()
    school_year = models.CharField(max_length=100, choices=SchoolYear_Choices, default='2023-2024')
    pictures = models.ImageField(upload_to='violations', null=True,blank=True)
    date_posted = models.DateTimeField(default=timezone.now,null=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT)
    intervention_date = models.DateTimeField(null=True, blank=True)
    action_taken = models.TextField(null=True, blank=True, choices=action_taken, default="Action Not Taken")
    recommendation = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Violation for {self.student.name}"

    def get_absolute_url(self):
        return reverse('disciplinetracking-list', kwargs={'pk':self.student.pk})

    @property
    def image_url(self):
        if self.image:
            return getattr(self.photo, 'url', None)
        return None