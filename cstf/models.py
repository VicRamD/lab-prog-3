from datetime import date, datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#Pasar modelos
#Docente, estudiante, asesor para otra app
class Docente(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    cuil = models.IntegerField()
    fecha_alta = models.DateField(blank=True)
    fecha_baja = models.DateField(blank=True)

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
    #asesor = models.ForeignKey(Asesor, on_delete=models.PROTECT, related_name="asesor")
    titulo = models.CharField(max_length=50)
    descripcion = models.TextField()
    proyecto_escrito = models.FileField()
    certificado_analítico = models.FileField()
    nota_director = models.FileField()
    cv = models.FileField()
    estado = models.CharField(choices=ESTADO_OPCIONES)
    #observaciones


class Estudiante(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.PROTECT, related_name="estudiante_proyecto")
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    dni = models.IntegerField()
    matricula = models.CharField(max_length=12)
    email = models.EmailField(max_length=45)


class Tribunal(models.Model):
    miembros = models.ManyToManyField(Docente, related_name="miembros")
    disposicion = models.FileField()
    fecha_disposicion = models.DateField()
    numero_disposicion = models.IntegerField()
    proyecto = models.OneToOneField(Proyecto, on_delete=models.PROTECT, related_name="tribunal_proyecto")


class Informe(models.Model):
    proyecto = models.OneToOneField(Proyecto, on_delete=models.PROTECT, related_name="informe_proyecto")
    fecha_de_entrega = models.DateField(auto_now_add=True)
    arch_evaluacion = models.FileField()
    # observaciones


class TrabajoFinal(models.Model):
    proyecto = models.OneToOneField(Proyecto, on_delete=models.PROTECT, related_name="tf_proyecto")
    borrador = models.FileField()
    aceptacion_director = models.FileField()
    fecha_presentacion = models.DateField(auto_now_add=True)
#Fecha manual

class EvaluacionTF(models.Model):
    trabajo_final = models.OneToOneField(TrabajoFinal, on_delete=models.PROTECT, related_name="evaluacion_tf")
    informe = models.FileField()
    fecha = models.DateField()


class Defensa(models.Model):
    trabajo_final = models.OneToOneField(TrabajoFinal, on_delete=models.PROTECT, related_name="defensa_tf")
    fecha = models.DateField()
    nota = models.IntegerField(blank=True)



