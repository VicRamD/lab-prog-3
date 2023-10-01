from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Estudiante(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    dni = models.IntegerField()
    matricula = models.CharField(max_length=12)
    email = models.EmailField(max_length=45)

class Docente(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    cuil = models.IntegerField()
