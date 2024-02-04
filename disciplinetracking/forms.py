from django import forms
from .models import Violation, Student
from bootstrap_datepicker_plus.widgets import DateTimePickerInput, DatePickerInput
from django.urls import reverse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

class StudentRegisterForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['lrn', 'name', 'birthday']

        widgets = {
            "birthday": DatePickerInput(),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['created_by'].widget = forms.HiddenInput()
    
    


class ViolationForm(forms.ModelForm):
    class Meta:
        model = Violation
        fields = ['school_year','date_committed','selected_offense','custom_description','narrative_report', 'pictures','action_taken', 'intervention_date', 'recommendation']

        widgets = {
            "date_posted": DateTimePickerInput(),
            "intervention_date": DateTimePickerInput(),
        }
    

    # def get_absolute_url(self):
    #     return reverse('disciplinetracking-list', kwargs={'pk':self.pk})
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['created_by'].widget = forms.HiddenInput()

class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
