#from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse

from gestion.models import Proyecto, Comision, InstanciaEvaluacion, Evaluacion
from gestion.forms import ProyectoForm
from persona.models import Estudiante, IntegranteProyecto, Asesor, Docente, RolProyecto, IntegranteComision,AsesorProyecto



# Create your views here.
def index(request):
    return render(request, 'index.html')

def agregarIntegranteProyecto(integrantes_seleccionados, proyecto):
    estudiantes_seleccionados = Estudiante.objects.filter(id__in=integrantes_seleccionados)
    for integrante in estudiantes_seleccionados:
        integrante_proyecto_instance = IntegranteProyecto(proyecto=proyecto,
                                                          estudiante=integrante,
                                                          fecha_alta=timezone.now(),
                                                          fecha_baja=None)
        integrante_proyecto_instance.save()
def agregarAsesorProyecto(asesor_seleccionado, proyecto):
    asesor = Asesor.objects.get(id=asesor_seleccionado)
    asesor_proyecto_instance = AsesorProyecto(proyecto=proyecto, asesor=asesor)
    asesor_proyecto_instance.save()

def agregarRolProyecto(docente_seleccionado, proyecto, rol):
    docente = Docente.objects.get(id=docente_seleccionado)
    director_proyecto_instance = RolProyecto(descripcion=rol,
                                             proyecto=proyecto,
                                             docente=docente,
                                             fecha_alta=timezone.now(),
                                             fecha_baja=None)
    director_proyecto_instance.save()

def agregarCSTFProyecto(comision_seleccionada, proyecto):
    docentes_seleccionados = Docente.objects.filter(id__in=comision_seleccionada)
    comision_instance = Comision(proyecto=proyecto)
    comision_instance.save()
    for docente in docentes_seleccionados:
        comision_proyecto_instance = IntegranteComision(comision=comision_instance,
                                                          docente=docente)
    comision_proyecto_instance.save()

def agregarInstanciaEvaluacion(descripcion, observacion, proyecto):
    instancia_evaluacion_instance = InstanciaEvaluacion(descripcion=descripcion, observacion=observacion, proyecto=proyecto)
    instancia_evaluacion_instance.save()
def seccionProyectos(request):
    proyectos = Proyecto.objects.all().order_by('-fecha_presentacion')
    return render(request, 'proyectos/proyectos.html',{'proyectos': proyectos})
def detalleProyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id=id)
    #instancias_evaluacion = InstanciaEvaluacion.objects.filter(proyecto=proyecto).latest('id')
    return render(request, 'proyectos/detalleProyecto.html',{'proyecto': proyecto})

def nuevoProyecto(request):
    if request.method == 'POST':
        form_proyecto = ProyectoForm(request.POST, request.FILES, prefix='proyecto')
        integrantes_seleccionados = request.POST.getlist('integrantesSelecionados')
        asesor_seleccionado = request.POST.getlist('asesor_seleccionado')
        director_seleccionado = request.POST.getlist('director_seleccionado')
        codirector_seleccionado = request.POST.getlist('codirector_seleccionado')
        comision_seleccionada = request.POST.getlist('comision_seleccionada')
        if form_proyecto.is_valid() and integrantes_seleccionados and asesor_seleccionado and director_seleccionado and codirector_seleccionado and comision_seleccionada:
            proyecto_instance = form_proyecto.save()
            agregarIntegranteProyecto(integrantes_seleccionados, proyecto_instance)
            agregarRolProyecto(director_seleccionado[0], proyecto_instance, 'Director')
            agregarRolProyecto(codirector_seleccionado[0], proyecto_instance, 'Codirector')
            agregarAsesorProyecto(asesor_seleccionado[0], proyecto_instance)
            agregarCSTFProyecto(comision_seleccionada, proyecto_instance)
            agregarInstanciaEvaluacion('COMISION DE SEGUIMIENTO',
                                       'Proyecto Final Presentado. En evaluación por la Comisión de Seguimiento de Trabajo Finales',
                                       proyecto_instance)

            messages.success(request, 'Se ha creado el proyecto correctamente.')
            #return redirect(reverse('gestion:detalle_proyecto', args={proyecto_instance.id}))
            return redirect('gestion:detalle_proyecto', proyecto_instance.id)
    else:
        form_proyecto = ProyectoForm(prefix='proyecto')

    estudiantes = Estudiante.objects.all()
    asesores = Asesor.objects.all()
    docentes = Docente.objects.all()
    return render(request, 'proyectos/nuevo_proyecto.html', {
        'form_proyecto': form_proyecto,
        'estudiantes': estudiantes,
        'asesores': asesores,
        'docentes': docentes
    })

def controlMovimiento(id, instancia_actual, estado, observacion_movimiento):
    proyecto = get_object_or_404(Proyecto, id=id)
    if estado == 'APROBADO':
        if instancia_actual == 'COMISION DE SEGUIMIENTO':
            agregarInstanciaEvaluacion('TRIBUNAL EVALUADOR', observacion_movimiento, proyecto)
        elif instancia_actual == 'TRIBUNAL EVALUADOR':
            agregarInstanciaEvaluacion('DEFENSA TRABAJO FINAL', observacion_movimiento, proyecto)
        elif instancia_actual == 'DEFENSA TRABAJO FINAL':
            agregarInstanciaEvaluacion('FINALIZADO', observacion_movimiento, proyecto)
    elif estado == 'OBSERVADO':
        if instancia_actual != 'FINALIZADO':
            agregarInstanciaEvaluacion(instancia_actual, observacion_movimiento, proyecto)
    elif estado == 'RECHAZADO':
        if instancia_actual != 'FINALIZADO':
            agregarInstanciaEvaluacion('FINALIZADO', observacion_movimiento, proyecto)

def agregarResultadoEvaluacion(id, informe, estado):
    proyecto = get_object_or_404(Proyecto, id=id)
    ultima_instancia = proyecto.proyecto_instancia.last()
    evaluacion_instance = Evaluacion(informe=informe,
                                     fecha=timezone.now(),
                                     estado=estado,
                                     instancia_evaluacion=ultima_instancia)
    evaluacion_instance.save()

def movimientos(request, id):
    proyecto = get_object_or_404(Proyecto, id=id)
    if request.method == 'POST':
        resultado_evaluacion = request.POST.get('estado')
        informe_evaluacion = request.FILES['informe']
        observacion_movimiento = request.POST.get('observacion', '')
        instancia_actual= proyecto.proyecto_instancia.last().descripcion
        if resultado_evaluacion and informe_evaluacion and observacion_movimiento:
            controlMovimiento(proyecto.id, instancia_actual, resultado_evaluacion,observacion_movimiento)
            agregarResultadoEvaluacion(proyecto.id, informe_evaluacion, resultado_evaluacion)
            messages.success(request, 'Se agregó la nueva instancia correctamente.')
            return redirect(reverse('gestion:movimientos', args={proyecto.id}))

    return render(request, 'movimientos/movimientos.html', {'proyecto': proyecto})

def estadisticas(request):
    return render(request, 'proyectos/eProyectos.html')

def seccionComision(request):
    return render(request, 'comision/proyectos_finales.html')

def comisionNuevoIntegrante(request):
    return render(request, 'comision/registro_CSTF.html')

