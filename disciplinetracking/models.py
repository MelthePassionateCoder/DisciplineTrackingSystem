from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

SchoolYear_Choices = (
    ('2019','SY2019-2020'),
    ('2020','SY2020-2021'),
    ('2021','SY2021-2022'),
    ('2022','SY2022-2023'),
    ('2023','SY2023-2024'),
)

class Student(models.Model):
    lrn = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    birthday = models.DateField()
    date_posted = models.DateTimeField(default=timezone.now,null=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('disciplinetracking-list', kwargs={'pk':self.pk})

class Violation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    narrative_report = models.TextField()
    school_year = models.CharField(max_length=100, choices=SchoolYear_Choices, default='2023')
    pictures = models.ImageField(upload_to='violations', null=True)
    date_posted = models.DateTimeField(default=timezone.now,null=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return f"Violation for {self.student.name}"

    def get_absolute_url(self):
        return reverse('disciplinetracking-list', kwargs={'pk':self.student.pk})