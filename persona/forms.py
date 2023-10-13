from django import forms
from persona.models import Estudiante, Persona

class NuevoEstudianteForm(forms.Form):

    class Meta:
        model = Estudiante
        fields = ['nombre', 'apellido', 'cuil', 'email', 'telefono', 'matricula']
        #fields = [__all__]


# class Persona(models.Model):
#     nombre = models.CharField(max_length=30)
#     apellido = models.CharField(max_length=30)
#     cuil = models.IntegerField()
#     dni = models.IntegerField()
#     email = models.EmailField(max_length=45)
#     telefono = models.CharField()

# class Docente(Persona):
#     fecha_alta = models.DateField(blank=True)
#     fecha_baja = models.DateField(blank=True)
#
#     def registrar_alta(self):
#         self.fecha_alta = date.today()
#
#     def registrar_baja(self):
#         self.fecha_baja = date.today()
# # Create your models here.
#
# class Estudiante(Persona):
#     matricula = models.CharField(max_length=12)
#
# class Asesor(Persona):
#     matricula = models.CharField(max_length=12)

