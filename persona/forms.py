from django import forms
from persona.models import Estudiante, Persona, Asesor, Docente
from django.core.exceptions import ValidationError

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

class AsesorForm(forms.ModelForm):
    class Meta:
        model = Asesor
        fields = ('nombre', 'apellido', 'cuil', 'email', 'telefono', 'cv')

        widgets = {
            'nombre': forms.TextInput(attrs={"id": "id_nombre"}),
            'apellido': forms.TextInput(attrs={"id": "id_apellido"}),
            'cuil': forms.TextInput(attrs={"id": "id_cuil"}),
            'email': forms.EmailInput(attrs={"id": "id_email"}),
            'telefono': forms.TextInput(attrs={"id": "id_telefono"}),
            'cv': forms.ClearableFileInput(attrs={"id": "id_cv"}),
        }

        def clean_requisitos(self):
            cv = self.cleaned_data['cv']
            if cv:
                extension = cv.name.rsplit('.', 1)[1].lower()
                if extension != 'pdf':
                    raise ValidationError('El archivo seleccionado no tiene el formato PDF.')
            return cv

class DocenteForm(forms.ModelForm):
    class Meta:
        model = Docente
        fields = ('nombre', 'apellido', 'cuil', 'email', 'telefono')

        widgets = {
            'nombre': forms.TextInput(attrs={"id": "id_nombre"}),
            'apellido': forms.TextInput(attrs={"id": "id_apellido"}),
            'cuil': forms.TextInput(attrs={"id": "id_cuil"}),
            'email': forms.EmailInput(attrs={"id": "id_email"}),
            'telefono': forms.TextInput(attrs={"id": "id_telefono"}),
        }