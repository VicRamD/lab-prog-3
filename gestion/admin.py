from django.contrib import admin
# Register your models here.
from gestion.models import InstanciaEvaluacion, Evaluacion, Proyecto, TrabajoFinal, Tribunal, Defensa, Comision


admin.site.register(InstanciaEvaluacion)
admin.site.register(Evaluacion)
admin.site.register(Proyecto)
admin.site.register(TrabajoFinal)
admin.site.register(Tribunal)
admin.site.register(Defensa)
admin.site.register(Comision)
'''
@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "descripcion")
'''