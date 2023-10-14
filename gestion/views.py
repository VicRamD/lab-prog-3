#from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse

from gestion.models import Proyecto, Comision, InstanciaEvaluacion, ComisionProyecto
from gestion.forms import ProyectoForm, EvaluacionForm, DefensaForm
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
    rol_proyecto_instance = RolProyecto(descripcion=rol,
                                             proyecto=proyecto,
                                             docente=docente,
                                             fecha_alta=timezone.now(),
                                             fecha_baja=None)
    rol_proyecto_instance.save()

def agregarCSTFProyecto(id_comision, proyecto):
    comision = get_object_or_404(Comision, id=id_comision)
    comision_instance = ComisionProyecto(proyecto=proyecto, comision=comision)
    comision_instance.save()

def agregarInstanciaEvaluacion(descripcion, proyecto):
    instancia_evaluacion_instance = InstanciaEvaluacion(descripcion=descripcion, proyecto=proyecto)
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
        if form_proyecto.is_valid() and integrantes_seleccionados and asesor_seleccionado and director_seleccionado and codirector_seleccionado:
            proyecto_instance = form_proyecto.save()
            agregarIntegranteProyecto(integrantes_seleccionados, proyecto_instance)
            agregarRolProyecto(director_seleccionado[0], proyecto_instance, 'Director')
            agregarRolProyecto(codirector_seleccionado[0], proyecto_instance, 'Codirector')
            agregarAsesorProyecto(asesor_seleccionado[0], proyecto_instance)
            agregarCSTFProyecto(comision_seleccionada[0], proyecto_instance)
            agregarInstanciaEvaluacion('COMISION DE SEGUIMIENTO', proyecto_instance)

            messages.success(request, 'Se ha creado el proyecto correctamente.')
            #return redirect(reverse('gestion:detalle_proyecto', args={proyecto_instance.id}))
            return redirect('gestion:detalle_proyecto', proyecto_instance.id)
    else:
        form_proyecto = ProyectoForm(prefix='proyecto')

    estudiantes = Estudiante.objects.all()
    asesores = Asesor.objects.all()
    docentes = Docente.objects.all()
    comisiones = Comision.objects.all()
    return render(request, 'proyectos/nuevo_proyecto.html', {
        'form_proyecto': form_proyecto,
        'estudiantes': estudiantes,
        'asesores': asesores,
        'docentes': docentes,
        'comisiones': comisiones
    })

def controlEstado(id):
    proyecto = get_object_or_404(Proyecto, id=id)
    ultimo_estado = proyecto.proyecto_instancia.last()
    ultima_evaluacion = ultimo_estado.instancia_evaluacion.last()
    if ultima_evaluacion.estado == 'APROBADO':
        if ultimo_estado.descripcion == 'COMISION DE SEGUIMIENTO':
            agregarInstanciaEvaluacion('TRIBUNAL EVALUADOR', proyecto)
        elif ultimo_estado.descripcion == 'TRIBUNAL EVALUADOR':
            agregarInstanciaEvaluacion('DEFENSA TRABAJO FINAL', proyecto)
        elif ultimo_estado.descripcion == 'DEFENSA TRABAJO FINAL':
            agregarInstanciaEvaluacion('FINALIZADO', proyecto)
    elif ultima_evaluacion.estado == 'RECHAZADO':
            agregarInstanciaEvaluacion('FINALIZADO', proyecto)

def movimientos(request, id):
    proyecto = get_object_or_404(Proyecto, id=id)
    if request.method == 'POST':
        form_evaluacion = EvaluacionForm(request.POST, request.FILES, prefix='evaluacion')
        form_defensa = DefensaForm(request.POST, request.FILES, prefix='defensa')
        instancia_actual= proyecto.proyecto_instancia.last()

        if form_evaluacion.is_valid():
            evaluacion_instance = form_evaluacion.save(commit=False)
            evaluacion_instance.fecha= timezone.now()
            evaluacion_instance.instancia_evaluacion= instancia_actual
            evaluacion_instance.save()
            controlEstado(proyecto.id)
            return redirect(reverse('gestion:movimientos', args={proyecto.id}))

        elif form_defensa.is_valid():
            print("antes de grabar defensa")
            defensa_instance = form_defensa.save(commit=False)
            defensa_instance.proyecto = proyecto
            defensa_instance.save()
            controlEstado(proyecto.id)
            return redirect(reverse('gestion:movimientos', args={proyecto.id}))

    else:
        form_evaluacion = EvaluacionForm(prefix='evaluacion')
        form_defensa = DefensaForm(prefix='defensa')

    return render(request, 'movimientos/movimientos.html', {
        'proyecto': proyecto,
        'form_evaluacion': form_evaluacion,
        'form_defensa': form_defensa})

def estadisticas(request):
    return render(request, 'proyectos/eProyectos.html')

def seccionComision(request):
    return render(request, 'comision/proyectos_finales.html')

def comisionNuevoIntegrante(request):
    return render(request, 'comision/registro_CSTF.html')

