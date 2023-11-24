from django import forms
from .models import Violation, Student
from bootstrap_datepicker_plus.widgets import DateTimePickerInput, DatePickerInput
from django.urls import reverse

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
        fields = ['narrative_report','school_year', 'pictures', 'date_posted','intervention_date', 'action_taken', 'recommendation']

        widgets = {
            "date_posted": DateTimePickerInput(),
            "intervention_date": DateTimePickerInput(),
        }
    

    # def get_absolute_url(self):
    #     return reverse('disciplinetracking-list', kwargs={'pk':self.pk})
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['created_by'].widget = forms.HiddenInput()

    