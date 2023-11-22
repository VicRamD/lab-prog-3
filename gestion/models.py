from django.db import models


class Proyecto(models.Model):
    titulo = models.CharField(max_length=50)
    descripcion = models.TextField()
    fecha_presentacion = models.DateField(blank=True)
    proyecto_escrito = models.FileField(upload_to='uploads/')
    certificado_analitico = models.FileField(upload_to='uploads/')
    nota_aceptacion = models.FileField(upload_to='uploads/')

    def __str__(self):
        return f"PTF-{self.id}"
class TrabajoFinal(models.Model):
    proyecto = models.OneToOneField(Proyecto, on_delete=models.PROTECT, related_name="tf_proyecto")
    borrador = models.FileField(upload_to='uploads/')
    aceptacion_director = models.FileField(upload_to='uploads/')
    fecha_presentacion = models.DateField()



class Tribunal(models.Model):
    disposicion = models.FileField(upload_to='uploads/')
    fecha_disposicion = models.DateField()
    numero_disposicion = models.CharField(max_length=50)
    proyecto = models.OneToOneField(Proyecto, on_delete=models.PROTECT, related_name="tribunal_proyecto")

class Defensa(models.Model):
    proyecto = models.OneToOneField(Proyecto, on_delete=models.CASCADE, related_name="defensa_proyecto", null=True, blank=True)
    fecha = models.DateField()
    nota = models.IntegerField(null=True, blank=True)
    acta = models.FileField(upload_to='uploads/', null=True, blank=True)

class Comision(models.Model):
    DESCRIPCION_DEPARTAMENTO = (
        ('Informatica', 'Informatica'),
        ('Minas', 'Minas'),
        ('Electronica', 'Electronica'),
        ('Agrimensura', 'Agrimensura'),
    )
    descripcion = models.CharField(max_length=70, default="Comisión nueva")
    resolucion = models.FileField(upload_to='uploads/', null=True, blank=True)
    departamento = models.CharField(max_length=20, choices=DESCRIPCION_DEPARTAMENTO, default="Informatica")

class ComisionProyecto(models.Model):
    proyecto = models.OneToOneField(Proyecto, on_delete=models.PROTECT, related_name="comision_proyecto")
    comision = models.ForeignKey(Comision, on_delete=models.PROTECT, related_name="proyecto_comision")
    fecha_alta = models.DateField()
class InstanciaEvaluacion(models.Model):
    DESCRIPCION_EVALUACION = (
        ('COMISION DE SEGUIMIENTO', 'COMISION DE SEGUIMIENTO'),
        ('TRIBUNAL EVALUADOR', 'TRIBUNAL EVALUADOR'),
        ('TRABAJO FINAL BORRADOR', 'TRABAJO FINAL BORRADOR'),
        ('DEFENSA TRABAJO FINAL', 'DEFENSA TRABAJO FINAL'),
        ('FINALIZADO', 'FINALIZADO'),
    )
    descripcion = models.CharField(max_length=30, choices=DESCRIPCION_EVALUACION)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name="proyecto_instancia")
class Evaluacion(models.Model):
    informe = models.FileField(upload_to='uploads/')
    fecha = models.DateField()
    ESTADO_OPCIONES = (
        ('OBSERVADO', 'OBSERVADO'),
        ('APROBADO', 'APROBADO'),
        ('RECHAZADO', 'RECHAZADO'),
    )
    estado = models.CharField(max_length=15, choices=ESTADO_OPCIONES)
    observacion = models.TextField()
    instancia_evaluacion = models.ForeignKey(InstanciaEvaluacion, on_delete=models.CASCADE, related_name="instancia_evaluacion")
    nuevoPTF = models.FileField(upload_to='uploads/', null=True, blank=True)
