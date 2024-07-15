from django import forms
from .models import BCISession, BCIData, Preprocessor, PreprocessingStep


class PreprocessorForm(forms.ModelForm):
    class Meta:
        model = Preprocessor
        fields = ['name', 'description']

class PreprocessingStepForm(forms.ModelForm):
    class Meta:
        model = PreprocessingStep
        fields = ['step_type', 'parameters']

class DataImportForm(forms.Form):
    file = forms.FileField()

class BCISessionForm(forms.ModelForm):
    class Meta:
        model = BCISession
        fields = ['session_name', 'date_recorded', 'subject_id']
        widgets = {
            'session_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_recorded': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'subject_id': forms.TextInput(attrs={'class': 'form-control'}),
        }

class BCIDataForm(forms.ModelForm):
    class Meta:
        model = BCIData
        fields = ['timestamp', 'channel_1', 'channel_2', 'channel_3', 'channel_4']
        widgets = {
            'timestamp': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'channel_1': forms.NumberInput(attrs={'class': 'form-control'}),
            'channel_2': forms.NumberInput(attrs={'class': 'form-control'}),
            'channel_3': forms.NumberInput(attrs={'class': 'form-control'}),
            'channel_4': forms.NumberInput(attrs={'class': 'form-control'}),
        }