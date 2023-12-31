from django.db import models
from gestion.models import Proyecto, Tribunal, Comision
from django.utils import timezone
from datetime import date

class Persona(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    cuil = models.CharField(max_length=12)
    dni = models.CharField(max_length=8)
    email = models.EmailField(max_length=45)
    telefono = models.CharField(max_length=15, blank=True)

    class Meta:
        abstract = True

    def nombre_completo(self):
        return self.apellido + " " + self.nombre

    def guardar_dni(self):
        cuil = self.cuil
        self.dni = cuil[2:10]

class Docente(Persona):
    '''fecha_alta = models.DateField(blank=True)
    fecha_baja = models.DateField(blank=True)

    def registrar_alta(self):
        self.fecha_alta = date.today()

    def registrar_baja(self):
        self.fecha_baja = date.today()'''

class Estudiante(Persona):
    matricula = models.CharField(max_length=12)

class Asesor(Persona):
    cv = models.FileField(upload_to='uploads/')

    def devolverCV(self):
        return self.cv

class AsesorProyecto(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.PROTECT, related_name="asesor_proyecto")
    asesor = models.ForeignKey(Asesor, on_delete=models.PROTECT, related_name="asesor")


class RolProyecto(models.Model):
    ROL_OPCIONES = (
        ('Director', 'Director'),
        ('Codirector', 'Codirector'),
    )
    descripcion = models.CharField(max_length=20, choices=ROL_OPCIONES)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.PROTECT, related_name="proyecto")
    docente = models.ForeignKey(Docente, on_delete=models.PROTECT, related_name="docente_proyecto")
    fecha_alta = models.DateField(blank=True)
    fecha_baja = models.DateField(blank=True, null=True)

class RolTribunal(models.Model):
    ROL_OPCIONES = (
        ('Presidente', 'Presidente'),
        ('Vocal', 'Vocal'),
        ('Vocal suplente', 'Vocal suplente'),
    )
    descripcion = models.CharField(max_length=20, choices=ROL_OPCIONES)
    tribunal = models.ForeignKey(Tribunal, on_delete=models.CASCADE, related_name="tribunal")
    docente = models.ForeignKey(Docente, on_delete=models.PROTECT, related_name="docente_tribunal")
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(default=date(9999, 12, 31))

class IntegranteProyecto(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.PROTECT, related_name="proyecto_integrante")
    estudiante = models.ForeignKey(Estudiante, on_delete=models.PROTECT, related_name="estudiante")
    fecha_alta = models.DateField(blank=True)
    fecha_baja = models.DateField(blank=True, null=True)
class IntegranteComision(models.Model):
    comision = models.ForeignKey(Comision, on_delete=models.PROTECT, related_name="comision")
    docente = models.ForeignKey(Docente, on_delete=models.PROTECT, related_name="integrante_comision")
    fecha_alta = models.DateField(default=timezone.now)