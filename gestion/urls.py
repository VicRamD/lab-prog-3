from django.urls import path

from gestion import views

app_name = 'gestion'
urlpatterns = [
    #path('', views.index, name='index'),
    path('proyectos/', views.seccionProyectos, name='proyectos'),
    path('proyectos/<int:id>/', views.detalleProyecto, name='detalle_proyecto'),
    path('proyectos/nuevo_proyecto', views.nuevoProyecto, name='nuevo_proyecto'),
    path('movimientos/<int:id>/', views.movimientos, name='movimientos'),
    #path('movimientos/evaluar/<int:id>/', views.evaluar, name='evaluar'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
    path('comision/', views.seccionComision, name='comision'),
    path('comision/nuevo_integrante', views.comisionNuevoIntegrante, name='nuevo_integrante')
]