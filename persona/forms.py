from django import forms
from persona.models import Estudiante, Persona, Asesor, Docente
from django.core.exceptions import ValidationError

#==================Para Estudiantes================================
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

    def clean_cuil(self):
         cuil = self.cleaned_data['cuil']
         if cuil:
             estudiantes_con_cuil = Estudiante.objects.filter(cuil=cuil)
             if estudiantes_con_cuil.count() != 0:
                 mensaje = "Hay un estudiante registrado con ese cuil: " + estudiantes_con_cuil[0].nombre_completo()
                 #raise ValidationError(mensaje)
                 raise forms.ValidationError(mensaje, code="cuil repetido", )
             docentes_con_cuil = Docente.objects.filter(cuil=cuil)
             if docentes_con_cuil.count() != 0:
                 mensaje = "Hay un docente registrado con ese cuil: " + estudiantes_con_cuil[0].nombre_completo()
                 #raise ValidationError(mensaje)
                 raise forms.ValidationError(mensaje, code="cuil repetido", )
             asesores_con_cuil = Asesor.objects.filter(cuil=cuil)
             if asesores_con_cuil.count() != 0:
                 mensaje = "Hay un asesor registrado con ese cuil: " + estudiantes_con_cuil[0].nombre_completo()
                 #raise ValidationError(mensaje)
                 raise forms.ValidationError(mensaje, code="cuil repetido", )
         return cuil

    def clean_matricula(self):
        matricula = self.cleaned_data['matricula']
        if matricula:
            estudiantes_con_matricula = Estudiante.objects.filter(matricula=matricula)
            if estudiantes_con_matricula.count() != 0:
                mensaje = "Hay un estudiante registrado con el cuil " + matricula + ": " + estudiantes_con_matricula[0].nombre_completo()
                raise forms.ValidationError(mensaje, code="matricula repetida", )
            return matricula

    def clean_email(self):
        email = self.cleaned_data['email']
        estudiantes_con_email = Estudiante.objects.filter(email=email)
        if estudiantes_con_email.count() != 0:
            mensaje = "Hay un estudiante registrado con el cuil " + email + ": " + estudiantes_con_email[0].nombre_completo()
            raise forms.ValidationError(mensaje, code="email repetido", )
        docentes_con_email = Docente.objects.filter(email=email)
        if docentes_con_email.count() != 0:
            mensaje = "Hay un docente registrado con el cuil " + email + ": " + docentes_con_email[0].nombre_completo()
            raise forms.ValidationError(mensaje, code="email repetido", )
        asesores_con_email = Asesor.objects.filter(email=email)
        if asesores_con_email.count() != 0:
            mensaje = "Hay un asesor registrado con el cuil " + email + ": " + asesores_con_email[0].nombre_completo()
            raise forms.ValidationError(mensaje, code="email repetido", )
        return email

    def clean(self):
        datos = super().clean()
        nombre = datos.get('nombre')
        apellido = datos.get('apellido')

        if len(nombre) == 0 or len(apellido) == 0:
            raise forms.ValidationError("Hay al menos un campo vacio que es requerido, deb completarlo", code="Sin completar", )

class EstudianteUpdateForm(forms.ModelForm):

    class Meta:
        model = Estudiante
        fields = ('nombre', 'apellido', 'email', 'telefono', 'matricula')
        #fields = [__all__]
        widgets = {
            'nombre': forms.TextInput(attrs={"id": "id_nombre"}),
            'apellido': forms.TextInput(attrs={"id": "id_apellido"}),
            #'cuil': forms.TextInput(attrs={"id": "id_cuil"}),
            'email': forms.EmailInput(attrs={"id": "id_email"}),
            'telefono': forms.TextInput(attrs={"id": "id_telefono"}),
            'matricula': forms.TextInput(attrs={"id": "id_matricula"}),
        }

    def clean(self):
        datos = super().clean()
        nombre = datos.get('nombre')
        apellido = datos.get('apellido')
        email = datos.get('email')
        matricula = datos.get('matricula')

        if len(nombre) == 0 or len(apellido) == 0 or len(email) == 0 or len(matricula) == 0:
            raise forms.ValidationError("Hay al menos un campo vacio que es requerido, deb completarlo", code="Sin completar", )

#==============================================================================
#======================Para Asesores===========================================
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

    def clean_cv(self):
        cv = self.cleaned_data['cv']
        if cv:
            extension = cv.name.rsplit('.', 1)[1].lower()
            if extension != 'pdf':
                raise ValidationError('El archivo seleccionado no tiene el formato PDF.')
        return cv

    def clean_cuil(self):
         cuil = self.cleaned_data['cuil']
         if cuil:
             estudiantes_con_cuil = Estudiante.objects.filter(cuil=cuil)
             if estudiantes_con_cuil.count() != 0:
                 mensaje = "Hay un estudiante registrado con ese cuil: " + estudiantes_con_cuil[0].nombre_completo()
                 #raise ValidationError(mensaje)
                 raise forms.ValidationError(mensaje, code="cuil repetido", )
             docentes_con_cuil = Docente.objects.filter(cuil=cuil)
             if docentes_con_cuil.count() != 0:
                 mensaje = "Hay un docente registrado con ese cuil: " + estudiantes_con_cuil[0].nombre_completo()
                 #raise ValidationError(mensaje)
                 raise forms.ValidationError(mensaje, code="cuil repetido", )
             asesores_con_cuil = Asesor.objects.filter(cuil=cuil)
             if asesores_con_cuil.count() != 0:
                 mensaje = "Hay un asesor registrado con ese cuil: " + estudiantes_con_cuil[0].nombre_completo()
                 #raise ValidationError(mensaje)
                 raise forms.ValidationError(mensaje, code="cuil repetido", )
         return cuil

class AsesorUpdateForm(forms.ModelForm):

    class Meta:
        model = Asesor
        fields = ('nombre', 'apellido', 'email', 'telefono', 'cv')
        #fields = [__all__]
        widgets = {
            'nombre': forms.TextInput(attrs={"id": "id_nombre"}),
            'apellido': forms.TextInput(attrs={"id": "id_apellido"}),
            'email': forms.EmailInput(attrs={"id": "id_email"}),
            'telefono': forms.TextInput(attrs={"id": "id_telefono"}),
            'cv': forms.ClearableFileInput(attrs={"id": "id_cv"}),
        }

    def clean_cv(self):
        cv = self.cleaned_data['cv']
        if cv:
            extension = cv.name.rsplit('.', 1)[1].lower()
            if extension != 'pdf':
                raise ValidationError('El archivo seleccionado no tiene el formato PDF.')
        return cv

    def clean(self):
        datos = super().clean()
        nombre = datos.get('nombre')
        apellido = datos.get('apellido')
        email = datos.get('email')

        if len(nombre) == 0 or len(apellido) == 0 or len(email) == 0:
            raise forms.ValidationError("Hay al menos un campo vacio que es requerido, deb completarlo", code="Sin completar", )

#==============================================================================
#======================Para Docentes===========================================
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

    def clean_cuil(self):
        cuil = self.cleaned_data['cuil']
        if cuil:
            estudiantes_con_cuil = Estudiante.objects.filter(cuil=cuil)
            if estudiantes_con_cuil.count() != 0:
                mensaje = "Hay un estudiante registrado con ese cuil: " + estudiantes_con_cuil[0].nombre_completo()
                # raise ValidationError(mensaje)
                raise forms.ValidationError(mensaje, code="cuil repetido", )
            docentes_con_cuil = Docente.objects.filter(cuil=cuil)
            if docentes_con_cuil.count() != 0:
                mensaje = "Hay un docente registrado con ese cuil: " + estudiantes_con_cuil[0].nombre_completo()
                # raise ValidationError(mensaje)
                raise forms.ValidationError(mensaje, code="cuil repetido", )
            asesores_con_cuil = Asesor.objects.filter(cuil=cuil)
            if asesores_con_cuil.count() != 0:
                mensaje = "Hay un asesor registrado con ese cuil: " + estudiantes_con_cuil[0].nombre_completo()
                # raise ValidationError(mensaje)
                raise forms.ValidationError(mensaje, code="cuil repetido", )
        return cuil

class DocenteUpdateForm(forms.ModelForm):

    class Meta:
        model = Docente
        fields = ('nombre', 'apellido', 'email', 'telefono')
        widgets = {
            'nombre': forms.TextInput(attrs={"id": "id_nombre"}),
            'apellido': forms.TextInput(attrs={"id": "id_apellido"}),
            'email': forms.EmailInput(attrs={"id": "id_email"}),
            'telefono': forms.TextInput(attrs={"id": "id_telefono"}),
        }

    def clean(self):
        datos = super().clean()
        nombre = datos.get('nombre')
        apellido = datos.get('apellido')
        email = datos.get('email')

        if len(nombre) == 0 or len(apellido) == 0 or len(email) == 0:
            raise forms.ValidationError("Hay al menos un campo vacio que es requerido, deb completarlo", code="Sin completar", )