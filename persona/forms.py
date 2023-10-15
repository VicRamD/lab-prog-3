from django import forms
from persona.models import Estudiante, Persona, Asesor, Docente

class EstudianteForm(forms.ModelForm):

    class Meta:
        model = Estudiante
        fields = ('nombre', 'apellido', 'cuil', 'email', 'telefono', 'matricula')
        #fields = [__all__]

class AsesorForm(forms.Form):
    class Meta:
        model = Asesor
        fields = ('nombre', 'apellido', 'cuil', 'email', 'telefono', 'cv')

class DocenteForm(forms.Form):
    class Meta:
        model = Docente
        fields = ('nombre', 'apellido', 'cuil', 'email', 'telefono')
