from django import forms
from .models import BCISession, BCIData

class BCISessionForm(forms.ModelForm):
    class Meta:
        model = BCISession
        fields = ['session_name', 'date_recorded', 'subject_id']

class BCIDataForm(forms.ModelForm):
    class Meta:
        model = BCIData
        fields = ['timestamp', 'channel_1', 'channel_2', 'channel_3', 'channel_4']