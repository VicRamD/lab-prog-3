from django.urls import path

from gestion import views

app_name = 'gestion'
urlpatterns = [
    #path('', views.index, name='index'),
    path('proyectos/', views.seccionProyectos, name='proyectos'),
    path('proyectos/<int:id>/', views.detalleProyecto, name='detalle_proyecto'),
    path('proyectos/nuevo_proyecto', views.nuevoProyecto, name='nuevo_proyecto'),
    path('movimientos/<int:id>/', views.movimientos, name='movimientos'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
    path('comision/', views.seccionComision, name='comision'),
    path('comision/nuevo_integrante', views.nuevaComision, name='nuevo_integrante'),
    path('comision/detalle-ntegrantes/<int:id>/', views.detalleIntegrantesComision, name='detalle_integrantes_comision'),
    path('comision/detalle-proyectos/<int:id>/', views.detalleProyectosComision, name='detalle_proyectos_comision')
]