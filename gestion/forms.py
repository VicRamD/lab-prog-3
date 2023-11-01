from django import forms
from django.forms import DateInput

from gestion.models import Proyecto, Defensa, Evaluacion, Comision,Tribunal


class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ('titulo','descripcion', 'fecha_presentacion', 'proyecto_escrito', 'certificado_analitico', 'nota_aceptacion')

        widgets = {
            'fecha_presentacion': DateInput(format='%d-m-Y%', attrs={'type': 'date'})
        }
class EvaluacionForm(forms.ModelForm):
    class Meta:
        model = Evaluacion
        fields = ('estado', 'informe', 'observacion')

class DefensaForm(forms.ModelForm):
    class Meta:
        model = Defensa
        fields = ('fecha', 'nota', 'acta')

        widgets = {
            'fecha': DateInput(format='%d-m-Y%', attrs={'type': 'date'})
        }
class ComisionForm(forms.ModelForm):
    class Meta:
        model = Comision
        fields = ('descripcion', 'resolucion', 'departamento')
class TribunalForm(forms.ModelForm):
    class Meta:
        model = Tribunal
        fields = ('numero_disposicion', 'fecha_disposicion', 'disposicion')

    widgets = {
        'fecha_disposicion': DateInput(format='%d-m-Y%', attrs={'type': 'date'})
    }

