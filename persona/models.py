from django.db import models
from gestion.models import Proyecto, Tribunal, Comision
from datetime import date

class Persona(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    cuil = models.IntegerField()
    dni = models.IntegerField()
    email = models.EmailField(max_length=45)
    telefono = models.CharField()

class Docente(Persona):
    fecha_alta = models.DateField(blank=True)
    fecha_baja = models.DateField(blank=True)

    def registrar_alta(self):
        self.fecha_alta = date.today()

    def registrar_baja(self):
        self.fecha_baja = date.today()

class Estudiante(Persona):
    matricula = models.CharField(max_length=12)

class Asesor(Persona):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.PROTECT, related_name="proyecto_asesor")


class RolProyecto(models.Model):
    ROL_OPCIONES = (
        ('director', 'DIRECTOR'),
        ('codirector', 'CODIRECTOR'),
    )
    descripcion = models.CharField(choices=ROL_OPCIONES)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.PROTECT, related_name="proyecto")
    docente = models.OneToOneField(Docente, on_delete=models.PROTECT, related_name="docente_proyecto")

class RolTribunal(models.Model):
    ROL_OPCIONES = (
        ('presidente', 'PRESIDENTE'),
        ('vocal', 'VOCAL'),
        ('vocal_suplente', 'VOCAL SUPLENTE'),
    )
    descripcion = models.CharField(choices=ROL_OPCIONES)
    tribunal = models.OneToOneField(Tribunal, on_delete=models.CASCADE, related_name="tribunal")
    docente = models.OneToOneField(Docente, on_delete=models.PROTECT, related_name="docente_tribunal")

class IntegranteProyecto(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.PROTECT, related_name="proyecto_integrante")
    estudiante = models.OneToOneField(Estudiante, on_delete=models.PROTECT, related_name="estudiante")
class IntegranteComision(models.Model):
    comision = models.ForeignKey(Comision, on_delete=models.PROTECT, related_name="comision")
    docente = models.ForeignKey(Docente, on_delete=models.PROTECT, related_name="integrante_comision")