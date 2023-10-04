from datetime import date, datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Docente(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    cuil = models.IntegerField()
    fecha_alta = models.DateTimeField()
    fecha_baja = models.DateTimeField()

    def registrar_alta(self):
        self.fecha_alta = date.today()

    def registrar_baja(self):
        self.fecha_baja = date.today()

class Proyecto(models.Model):
    ESTADO_OPCIONES = (
        ('pendiente', 'PENDIENTE'),
        ('observado', 'OBSERVADO'),
        ('rechazado', 'RECHAZADO'),
    )

    director = models.ForeignKey(Docente, on_delete=models.PROTECT, related_name="director")
    codirector = models.ForeignKey(Docente, on_delete=models.PROTECT, related_name="codirector")
    asesor = models.ForeignKey(Docente, on_delete=models.PROTECT, related_name="asesor")
    titulo = models.CharField(max_length=50)
    descripcion = models.TextField()
    proyecto_escrito = models.FileField()
    certificado_analítico = models.FileField()
    nota_director = models.FileField()
    cv = models.FileField()
    estado = models.CharField(choices=ESTADO_OPCIONES)

class Estudiante(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.PROTECT, related_name="proyecto")
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    dni = models.IntegerField()
    matricula = models.CharField(max_length=12)
    email = models.EmailField(max_length=45)


