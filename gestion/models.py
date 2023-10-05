from django.db import models

from persona.models import Docente, Asesor


# Create your models here.


class Instancia_evaluacion(models.Model):
    DESCRIPCION_EVALUACION = (
        ('comision', 'COMISION DE SEGUIMIENTO'),
        ('tribunal', 'TRIBUNAL EVALUADOR'),
        ('defensa', 'DEFENSA TRABAJO FINAL'),
        ('finalizado', 'FINALIZADO'),
    )
    descripcion = models.CharField(choices=DESCRIPCION_EVALUACION)
    observacion = models.TextField()
class Evaluacion(models.Model):
    informe = models.FileField()
    fecha = models.DateField()
    ESTADO_OPCIONES = (
        ('pendiente', 'PENDIENTE'),
        ('aprobado', 'APROBADO'),
        ('rechazado', 'RECHAZADO'),
    )
    estado = models.CharField(choices=ESTADO_OPCIONES)
    instancia_evaluacion = models.OneToOneField(Instancia_evaluacion, on_delete=models.PROTECT, related_name="instancia_evaluacion", blank=True)


class Proyecto(models.Model):
    director = models.ForeignKey(Docente, on_delete=models.PROTECT, related_name="director")
    codirector = models.ForeignKey(Docente, on_delete=models.PROTECT, related_name="codirector")
    asesor = models.ForeignKey(Asesor, on_delete=models.PROTECT, related_name="asesor")
    titulo = models.CharField(max_length=50)
    descripcion = models.TextField()
    fecha_presentacion = models.DateField(blank=True)
    proyecto_escrito = models.FileField()
    certificado_analitico = models.FileField()
    nota_aceptacion = models.FileField()
    cv = models.FileField()
    instancia = models.ForeignKey(Instancia_evaluacion, on_delete=models.PROTECT, related_name="instancia")
    estudiantes = models.ManyToManyField(Docente, related_name="estudiantes")
class TrabajoFinal(models.Model):
    proyecto = models.OneToOneField(Proyecto, on_delete=models.PROTECT, related_name="tf_proyecto")
    borrador = models.FileField()
    aceptacion_director = models.FileField()
    fecha_presentacion = models.DateField(auto_now_add=True)
    # Fecha manual


class Tribunal(models.Model):
    presidente = models.ForeignKey(Docente, on_delete=models.PROTECT, related_name="presidente")
    vocales = models.ManyToManyField(Docente, related_name="vocales")
    vocales_suplentes = models.ManyToManyField(Docente, related_name="vocales_suplentes")
    disposicion = models.FileField()
    fecha_disposicion = models.DateField()
    numero_disposicion = models.IntegerField()
    proyecto = models.OneToOneField(Proyecto, on_delete=models.PROTECT, related_name="tribunal_proyecto")


class Defensa(models.Model):
    trabajo_final = models.OneToOneField(TrabajoFinal, on_delete=models.PROTECT, related_name="defensa_tf")
    fecha = models.DateField()
    nota = models.IntegerField(blank=True)
    acta = models.FileField()
