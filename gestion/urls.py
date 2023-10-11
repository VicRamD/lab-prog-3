from django.urls import path

from gestion import views

app_name = 'gestion'
urlpatterns = [
    path('', views.index, name='index'),
    path('proyectos/', views.seccionProyectos, name='proyectos'),
    path('proyectos/nuevo_proyecto', views.nuevoProyecto, name='nuevo_proyecto'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
    path('comision/', views.seccionComision, name='comision'),
    path('comision/nuevo_integrante', views.comisionNuevoIntegrante, name='nuevo_integrante')
]