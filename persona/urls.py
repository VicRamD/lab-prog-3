from django.urls import path

from persona import views

app_name = 'persona'
urlpatterns = [
    path('estudiantes/crear/', views.nuevoEstudiante, name='nuevo_estudiante'),
    path('estudiantes/<int:pk>/', views.estudianteDetalle, name='detalle_estudiante'),
    path('asesores/crear/', views.nuevoAsesor, name='nuevo_asesor'),
    path('asesores/<int:pk>/', views.asesorDetalle, name='detalle_asesor'),
    path('docentes/crear/', views.nuevoDocente, name='nuevo_docente'),
    path('docentes/<int:pk>/', views.docenteDetalle, name='detalle_docente'),
]