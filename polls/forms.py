from django import forms
from .models import Course, Section

class courseForm(forms.ModelForm):

    dept_name = forms.ModelChoiceField(queryset=Course.objects.all().values_list('dept_name', flat=True).distinct(), label='Department Name')
    year = forms.ModelChoiceField(queryset=Section.objects.all().values_list('year', flat=True).distinct(), label='Year')
    semester = forms.ModelChoiceField(queryset=Section.objects.all().values_list('semester', flat=True).distinct(), label='Semester')

    class Meta:
        model = Course
        fields = ['dept_name', 'year', 'semester']