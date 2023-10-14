from django import forms
from django.forms import DateInput

from gestion.models import Proyecto, InstanciaEvaluacion, Evaluacion


class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ('titulo','descripcion', 'fecha_presentacion', 'proyecto_escrito', 'certificado_analitico', 'nota_aceptacion')

        widgets = {
            'fecha_presentacion': DateInput(format='%d-m-Y%',attrs={'type': 'date'})
        }
