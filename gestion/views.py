#from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from datetime import datetime

from gestion.models import Proyecto, Comision, InstanciaEvaluacion, ComisionProyecto, Tribunal
from gestion.forms import ProyectoForm, EvaluacionForm, DefensaForm, ComisionForm,TribunalForm
from persona.models import Estudiante, IntegranteProyecto, Asesor, Docente, RolProyecto, IntegranteComision, AsesorProyecto, RolTribunal



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
    comision_instance = ComisionProyecto(proyecto=proyecto, comision=comision, fecha_alta=timezone.now())
    comision_instance.save()

def agregarInstanciaEvaluacion(descripcion, proyecto):
    instancia_evaluacion_instance = InstanciaEvaluacion(descripcion=descripcion, proyecto=proyecto)
    instancia_evaluacion_instance.save()

def filtrarProyectoPorEstado(estado):
    if estado != 'TODOS':
        instancias_filtradas = InstanciaEvaluacion.objects.filter(descripcion=estado)
        proyectos_asociados = Proyecto.objects.filter(proyecto_instancia__in=instancias_filtradas).order_by('-fecha_presentacion')
        proyectos_lista = list(proyectos_asociados)
    else:
        proyectos_lista = Proyecto.objects.all().order_by('-fecha_presentacion')
    return proyectos_lista

def filtrarProyectoPorRango(fecha_desde, fecha_hasta):
    formato_fecha = "%Y-%m-%d"
    fecha_desde = datetime.strptime(fecha_desde, formato_fecha).date()
    fecha_hasta = datetime.strptime(fecha_hasta, formato_fecha).date()
    proyectos_en_rango = Proyecto.objects.filter(fecha_presentacion__range=(fecha_desde, fecha_hasta))
    return proyectos_en_rango.order_by('-fecha_presentacion')

def filtrarProyectoEstadoYRango(estado,fecha_desde, fecha_hasta):
    proyectos_rango = filtrarProyectoPorRango(fecha_desde, fecha_hasta)
    instancias_filtradas = InstanciaEvaluacion.objects.filter(descripcion=estado)
    proyectos_asociados = proyectos_rango.filter(proyecto_instancia__in=instancias_filtradas).order_by('-fecha_presentacion')
    return proyectos_asociados
def seccionProyectos(request):
    if request.method == 'POST':
        estado_seleccionado = request.POST.get('estado_seleccionado')
        fecha_desde = request.POST.get('fecha_desde')
        fecha_hasta = request.POST.get('fecha_hasta')
        if estado_seleccionado != 'TODOS' and fecha_desde and fecha_hasta:
            proyectos_lista = filtrarProyectoEstadoYRango(estado_seleccionado,fecha_desde, fecha_hasta)
        elif estado_seleccionado:
            proyectos_lista = filtrarProyectoPorEstado(estado_seleccionado)
        elif fecha_desde and fecha_hasta:
            proyectos_lista = filtrarProyectoPorRango(fecha_desde, fecha_hasta)

        return render(request, 'proyectos/proyectos.html', {'proyectos': proyectos_lista})

    proyectos = Proyecto.objects.all().order_by('-fecha_presentacion')
    return render(request, 'proyectos/proyectos.html',{'proyectos': proyectos})
def detalleProyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id=id)
    id_comision = proyecto.comision_proyecto.comision.id
    id_tribunal = proyecto.tribunal_proyecto.id
    return render(request, 'proyectos/detalleProyecto.html',{
        'proyecto': proyecto,
        'id_comision': id_comision,
        'id_tribunal': id_tribunal})

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
    comisiones = Comision.objects.all()
    return render(request, 'comision/comision_seguimiento.html',{'comisiones':comisiones})

def agregarIntegranteComision(integrantes, comision):
    docentes_seleccionados = Docente.objects.filter(id__in=integrantes)
    for integrante in docentes_seleccionados:
        integrante_comision_instance = IntegranteComision(comision=comision,
                                                          docente=integrante,
                                                          fecha_alta=timezone.now())
        integrante_comision_instance.save()

def nuevaComision(request):
    if request.method == 'POST':
        form_comision = ComisionForm(request.POST, request.FILES)
        integrantes_seleccionados = request.POST.getlist('integrantesSelecionados')
        if form_comision.is_valid() and integrantes_seleccionados:
            comision_instance = form_comision.save()
            agregarIntegranteComision(integrantes_seleccionados, comision_instance)

            messages.success(request, 'Se ha creado el comision correctamente.')
            return redirect('gestion:detalle_integrante_comision', comision_instance.id)
    else:
        form_comision = ComisionForm()

    docentes = Docente.objects.all()
    return render(request, 'comision/registro_CSTF.html', {
        'form_comision': form_comision,
        'docentes': docentes,
    })
def detalleIntegrantesComision(request, id):
    comision = get_object_or_404(Comision, id=id)
    return render(request, 'comision/detalleIntegrantes.html',{'comision': comision})
def detalleProyectosComision(request, id):
    comision = get_object_or_404(Comision, id=id)
    return render(request, 'comision/detalleProyectos.html',{'comision': comision})


def seccionTribunales(request):
    tribunales = Tribunal.objects.all().order_by('-fecha_disposicion')
    return render(request, 'tribunales/tribunales.html',{'tribunales':tribunales})
def detalleIntegrantesTribunal(request, id):
    tribunal = get_object_or_404(Tribunal, id=id)
    return render(request, 'tribunales/detalleIntegrantes.html',{'tribunal': tribunal})
def detalleProyectosTribunal(request, id):
    tribunal = get_object_or_404(Tribunal, id=id)
    return render(request, 'tribunales/detalleProyectos.html',{'tribunal': tribunal})
def agregarIntegrantesTribunal(integrantes, tribunal,rol):
    docentes_seleccionados = Docente.objects.filter(id__in=integrantes)
    for integrante in docentes_seleccionados:
        integrante_tribunal_instance = RolTribunal(descripcion=rol,
                                                   tribunal=tribunal,
                                                   docente=integrante,
                                                   fecha_alta=timezone.now())
        integrante_tribunal_instance.save()
def nuevoTribunal(request):
    if request.method == 'POST':
        form_tribunal = TribunalForm(request.POST, request.FILES, prefix='tribunal')
        presidente_seleccionado = request.POST.getlist('presidente_seleccionado')
        vocales_seleccionados = request.POST.getlist('vocales_seleccionados')
        vocales_suplentes_seleccionados = request.POST.getlist('vocales_suplentes_seleccionados')
        if form_tribunal.is_valid() and presidente_seleccionado and vocales_seleccionados and vocales_suplentes_seleccionados:
            tribunal_instance = form_tribunal.save()
            agregarIntegrantesTribunal(presidente_seleccionado, tribunal_instance,'Presidente')
            agregarIntegrantesTribunal(vocales_seleccionados, tribunal_instance, 'Vocal')
            agregarIntegrantesTribunal(vocales_suplentes_seleccionados, tribunal_instance, 'Vocal suplente')

            messages.success(request, 'Se ha creado el tribunal correctamente.')
            return redirect('gestion:detalle_integrante_tribunal', tribunal_instance.id)
    else:
        form_tribunal = TribunalForm(prefix='tribunal')

    docentes = Docente.objects.all()
    return render(request, 'tribunales/registro.html', {
        'form_tribunal': form_tribunal,
        'docentes': docentes,
    })