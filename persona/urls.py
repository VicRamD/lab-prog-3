from django.urls import path

from persona import views

app_name = 'persona'
urlpatterns = [
    path('estudiantes/crear/', views.nuevoEstudiante, name='nuevo_estudiante'),
    path('estudiantes/<int:pk>/', views.estudianteDetalle, name='detalle_estudiante'),
]