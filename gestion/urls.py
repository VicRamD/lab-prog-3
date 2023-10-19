from django.urls import path

from gestion import views

app_name = 'gestion'
urlpatterns = [
    #path('', views.index, name='index'),
    path('proyectos/', views.seccionProyectos, name='proyectos'),
    path('proyectos/nuevo_proyecto', views.nuevoProyecto, name='nuevo_proyecto'),
    path('proyectos/detalle-proyecto/<int:id>/', views.detalleProyecto, name='detalle_proyecto'),
    path('movimientos/<int:id>/', views.movimientos, name='movimientos'),
    path('movimientos/cargar-nuevo-PTF/<int:id>/', views.cargarNuevoPTF, name='cargar-nuevo-PTF'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
    path('comision/', views.seccionComision, name='comision'),
    path('comision/nuevo_integrante', views.nuevaComision, name='nuevo_integrante'),
    path('comision/detalle-integrantes/<int:id>/', views.detalleIntegrantesComision, name='detalle_integrantes_comision'),
    path('comision/detalle-proyectos/<int:id>/', views.detalleProyectosComision, name='detalle_proyectos_comision'),
    path('tribunales/', views.seccionTribunales, name='tribunales'),
    path('tribunales/nuevo_tribunal/<int:id>/', views.nuevoTribunal, name='nuevo_tribunal'),
    path('tribunales/detalle-integrantes/<int:id>/', views.detalleIntegrantesTribunal, name='detalle_integrantes_tribunal')
]