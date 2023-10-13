from django.contrib import admin
# Register your models here.
from persona.models import Docente, Estudiante, Asesor, RolProyecto, RolTribunal, IntegranteProyecto, IntegranteComision

#from apps.gestion.models import Proyecto

admin.site.register(Docente)
admin.site.register(Estudiante)
admin.site.register(Asesor)
admin.site.register(RolProyecto)
admin.site.register(RolTribunal)
admin.site.register(IntegranteProyecto)
admin.site.register(IntegranteComision)