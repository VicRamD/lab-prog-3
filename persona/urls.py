from django.urls import path

from persona import views

app_name = 'persona'
urlpatterns = [
    path('', views.listadoPersonas, name='lista_personas'),
    path('estudiantes/crear/', views.nuevoEstudiante, name='nuevo_estudiante'),
    path('estudiantes/<int:pk>/', views.estudianteDetalle, name='detalle_estudiante'),
    path('estudiantes/editar/<int:pk>', views.estudianteModificar, name='editar_estudiante'),
    path('asesores/crear/', views.nuevoAsesor, name='nuevo_asesor'),
    path('asesores/<int:pk>/', views.asesorDetalle, name='detalle_asesor'),
    path('asesores/editar/<int:pk>/', views.asesorModificar, name='editar_asesor'),
    path('docentes/crear/', views.nuevoDocente, name='nuevo_docente'),
    path('docentes/<int:pk>/', views.docenteDetalle, name='detalle_docente'),
    path('docentes/editar/<int:pk>/', views.docenteModificar, name='editar_docente'),
]