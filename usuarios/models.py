from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from persona.models import Estudiante, Asesor, Docente

class Usuario_persona(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name="persona_user")
    estudiante = models.OneToOneField(Estudiante, on_delete=models.PROTECT, related_name="usuario_estudiante", null=True, blank=True)
    asesor = models.OneToOneField(Asesor, on_delete=models.PROTECT, related_name="usuario_asesor", null=True, blank=True)
    docente = models.OneToOneField(Docente, on_delete=models.PROTECT, related_name="usuario_docente", null=True, blank=True)
    tipo = models.CharField(max_length=15, null=True, blank=True)

class Usuario_estudiante(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name="estudiante_user")
    estudiante = models.OneToOneField(Estudiante, on_delete=models.PROTECT, related_name="estudiante_usuario")
    tipo = "estudiante"

    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Usuario_estudiante.objects.create(user=instance)
    #
    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.profile.save()
class Usuario_docente(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name="docente_user")
    docente = models.OneToOneField(Docente, on_delete=models.PROTECT, related_name="docente_usuario")
    tipo = "docente"

class Usuario_asesor(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name="asesor_user")
    asesor = models.OneToOneField(Asesor, on_delete=models.PROTECT, related_name="asesor_usuario")
    tipo = "asesor"