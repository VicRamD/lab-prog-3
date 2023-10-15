from django import forms
from persona.models import Estudiante, Persona, Asesor, Docente

class EstudianteForm(forms.ModelForm):

    class Meta:
        model = Estudiante
        fields = ('nombre', 'apellido', 'cuil', 'email', 'telefono', 'matricula')
        #fields = [__all__]
        widgets = {
            'nombre': forms.TextInput(attrs={"id": "id_nombre"}),
            'apellido': forms.TextInput(attrs={"id": "id_apellido"}),
            'cuil': forms.TextInput(attrs={"id": "id_cuil"}),
            'email': forms.EmailInput(attrs={"id": "id_email"}),
            'telefono': forms.TextInput(attrs={"id": "id_telefono"}),
            'matricula': forms.TextInput(attrs={"id": "id_matricula"}),
        }

class AsesorForm(forms.Form):
    class Meta:
        model = Asesor
        fields = ('nombre', 'apellido', 'cuil', 'email', 'telefono', 'cv')

class DocenteForm(forms.Form):
    class Meta:
        model = Docente
        fields = ('nombre', 'apellido', 'cuil', 'email', 'telefono')
