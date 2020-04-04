from django import forms
from django.forms import inlineformset_factory

from monitoring import choices
from . import models

class HealthCenterForm(forms.ModelForm):
    class Meta:
        model = models.HealthCenter
        fields = '__all__'

class HealthCenterStatusForm(forms.ModelForm):
    class Meta:
        model = models.HealthCenterStatus
        exclude = ('beds', 'icus', 'respirators', 'occupied_beds', 'occupied_icus', 'occupied_respirators',)
        labels = {
            'health_center': 'Unidade de Saúde'
        }