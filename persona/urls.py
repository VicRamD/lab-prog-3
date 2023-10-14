from django.urls import path

from persona import views

app_name = 'persona'
urlpatterns = [
    path('estudiantes/crear/', views.nuevoEstudiante, name='nuevo_estudiante'),
    path('estudiantes/<int:id>', views.nuevoEstudiante, name='detalle_estudiante'),
    #path('logout', views.logout_view, name='logout')
]