from django.db import models
from django.conf import settings

# Create your models here.



class Proyecto(models.Model):
    titulo = models.CharField(max_length=50)
    descripcion = models.TextField()
    fecha_presentacion = models.DateField(blank=True)
    proyecto_escrito = models.FileField(upload_to='uploads/')
    certificado_analitico = models.FileField(upload_to='uploads/')
    nota_aceptacion = models.FileField(upload_to='uploads/')
class TrabajoFinal(models.Model):
    proyecto = models.OneToOneField(Proyecto, on_delete=models.PROTECT, related_name="tf_proyecto")
    borrador = models.FileField(upload_to='uploads/')
    aceptacion_director = models.FileField(upload_to='uploads/')
    fecha_presentacion = models.DateField()


class Tribunal(models.Model):
    disposicion = models.FileField(upload_to='uploads/')
    fecha_disposicion = models.DateField()
    numero_disposicion = models.IntegerField()
    proyecto = models.OneToOneField(Proyecto, on_delete=models.PROTECT, related_name="tribunal_proyecto")


class Defensa(models.Model):
    proyecto = models.OneToOneField(Proyecto, on_delete=models.CASCADE, related_name="defensa_proyecto", null=True, blank=True)
    fecha = models.DateField()
    nota = models.IntegerField()
    acta = models.FileField(upload_to='uploads/')

class Comision(models.Model):
    proyecto = models.OneToOneField(Proyecto, on_delete=models.PROTECT, related_name="comision_proyecto")

class InstanciaEvaluacion(models.Model):
    DESCRIPCION_EVALUACION = (
        ('COMISION DE SEGUIMIENTO', 'COMISION DE SEGUIMIENTO'),
        ('TRIBUNAL EVALUADOR', 'TRIBUNAL EVALUADOR'),
        ('DEFENSA TRABAJO FINAL', 'DEFENSA TRABAJO FINAL'),
        ('FINALIZADO', 'FINALIZADO'),
    )
    descripcion = models.CharField(choices=DESCRIPCION_EVALUACION)
    observacion = models.TextField()
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name="proyecto_instancia", null=True, blank=True)
class Evaluacion(models.Model):
    informe = models.FileField(upload_to='uploads/')
    fecha = models.DateField()
    ESTADO_OPCIONES = (
        ('pendiente', 'OBSERVADO'),
        ('aprobado', 'APROBADO'),
        ('rechazado', 'RECHAZADO'),
    )
    estado = models.CharField(choices=ESTADO_OPCIONES)
    instancia_evaluacion = models.OneToOneField(InstanciaEvaluacion, on_delete=models.CASCADE, related_name="instancia_evaluacion", blank=True)