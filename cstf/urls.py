from django.urls import path

from cstf import views

app_name = 'cstf'
urlpatterns = [
    path('', views.index, name='index'),
    path('proyectos/', views.seccionProyectos, name='proyectos'),
    path('proyectos/nuevo_proyecto', views.nuevoProyecto, name='nuevo_proyecto'),
    path('estadisticas/', views.estadisticas, name='estadisticas')
]