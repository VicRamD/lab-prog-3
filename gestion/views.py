# from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from datetime import datetime
import os
from django.db.models import OuterRef, Subquery

from gestion.models import Proyecto, Comision, InstanciaEvaluacion, ComisionProyecto, Tribunal, Evaluacion
from gestion.forms import ProyectoForm, EvaluacionForm, DefensaForm, ComisionForm, TribunalForm
from persona.models import Estudiante, IntegranteProyecto, Asesor, Docente, RolProyecto, IntegranteComision, \
    AsesorProyecto, RolTribunal
from usuarios.views import asignarUsuariosGrupo, es_asesor, es_comision, es_tribunal, es_estudiante, es_departamento, \
    es_docente, es_movimientos


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
    proyectos = Proyecto.objects.all().order_by('-fecha_presentacion')
    proyectos_lista = []
    if estado == 'TODOS':
        proyectos_lista = proyectos
    else:
        for proyecto in proyectos:
            if proyecto.proyecto_instancia.last().descripcion == estado:
                proyectos_lista.append(proyecto)

    return proyectos_lista


def filtrarProyectoPorRango(fecha_desde, fecha_hasta):
    formato_fecha = "%Y-%m-%d"
    fecha_desde = datetime.strptime(fecha_desde, formato_fecha).date()
    fecha_hasta = datetime.strptime(fecha_hasta, formato_fecha).date()
    proyectos_en_rango = Proyecto.objects.filter(fecha_presentacion__range=(fecha_desde, fecha_hasta))
    return proyectos_en_rango.order_by('-fecha_presentacion')


def filtrarProyectoEstadoYRango(estado, fecha_desde, fecha_hasta):
    proyectos_estado = filtrarProyectoPorEstado(estado)
    formato_fecha = "%Y-%m-%d"
    fecha_desde = datetime.strptime(fecha_desde, formato_fecha).date()
    fecha_hasta = datetime.strptime(fecha_hasta, formato_fecha).date()

    proyectos_en_rango = []

    for proyecto in proyectos_estado:
        if fecha_desde <= proyecto.fecha_presentacion <= fecha_hasta:
            proyectos_en_rango.append(proyecto)

    return proyectos_en_rango


def seccionProyectos(request):
    proyectos = Proyecto.objects.all().order_by('-fecha_presentacion')
    if request.method == 'POST':
        estado_seleccionado = request.POST.get('estado_seleccionado')
        fecha_desde = request.POST.get('fecha_desde')
        fecha_hasta = request.POST.get('fecha_hasta')
        proyectos_lista = proyectos
        print("antes de if")
        if estado_seleccionado != 'TODOS' and fecha_desde and fecha_hasta:
            print("Primer if")
            proyectos_lista = filtrarProyectoEstadoYRango(estado_seleccionado, fecha_desde, fecha_hasta)
        elif estado_seleccionado != 'TODOS':
            print("Segundo")
            proyectos_lista = filtrarProyectoPorEstado(estado_seleccionado)
        elif fecha_desde and fecha_hasta:
            print("antes de filtrar")
            proyectos_lista = filtrarProyectoPorRango(fecha_desde, fecha_hasta)

        return render(request, 'proyectos/proyectos.html', {'proyectos': proyectos_lista})

    return render(request, 'proyectos/proyectos.html', {'proyectos': proyectos})


def verificar_tiene_tribunal(proyecto_id):
    try:
        proyecto = Proyecto.objects.get(id=proyecto_id)
        print(proyecto)
        tribunal = proyecto.tribunal_proyecto
        return True
    except Proyecto.tribunal_proyecto.RelatedObjectDoesNotExist:
        print(proyecto.tribunal_proyecto.id)
        return False


def detalleProyecto(request, id):
    try:
        proyecto = get_object_or_404(Proyecto, id=id)
        id_tribunal = proyecto.tribunal_proyecto.id
        return render(request, 'proyectos/detalleProyecto.html', {
            'proyecto': proyecto,
            'tribunal_true': id_tribunal})
    except Proyecto.tribunal_proyecto.RelatedObjectDoesNotExist:
        messages.success(request, 'El usuario no tiene tribunal. Por favor asigne un tribunal.')
        return render(request, 'proyectos/detalleProyecto.html', {
            'proyecto': proyecto,
            'tribunal_true': False})

@login_required
def proyecto_edit(request, id):
    proyecto = Proyecto.objects.get(id=id)
    if request.method == 'POST':
        form_proyecto = ProyectoForm(request.POST, request.FILES, instance=proyecto)
        form_proyecto.save()
        messages.success(request, 'Se ha actualizado correctamente el Proyecto')
        return redirect(reverse('gestion:detalle_proyecto', args=[proyecto.id]))
    else:
        form_proyecto = ProyectoForm(instance=proyecto)
    return render(request, 'proyectos/proyecto_edit.html', {'form_proyecto': form_proyecto,
                                                            'proyecto': proyecto})
#===================================================
#===================================================
def obtenerIntegrantes(proyecto):
    estudiantes = Estudiante.objects.all()
    estudiantes_selecionados = proyecto.proyecto_integrante.all()
    docentes = Docente.objects.all()
    rolProyecto = proyecto.proyecto.all()
    for rol in rolProyecto:
        if rol.descripcion == 'Director':
            director = rol
        else:
            codirector = rol
    asesores = Asesor.objects.all()
    asesor_proyecto = proyecto.asesor_proyecto.all()
    for asesorp in asesor_proyecto:
        asesor = asesorp
    comisiones = Comision.objects.all()
    comision = proyecto.comision_proyecto
    return estudiantes, estudiantes_selecionados,docentes, director, codirector, asesores, asesor, comisiones, comision

def modificarIntegranteProyecto(integrantes_seleccionados, proyecto):
    estudiantes_actuales = proyecto.proyecto_integrante.all()
    estudiantes_seleccionados = Estudiante.objects.filter(id__in=integrantes_seleccionados)
    nuevosIntegrantes = []
    # Verificar si hay integrantes a eliminar
    integrantes_a_eliminar = []
    for integrante_actual in estudiantes_actuales:
        if integrante_actual.estudiante not in estudiantes_seleccionados:
            integrantes_a_eliminar.append(integrante_actual)
    # Eliminar integrantes no seleccionados
    for integrante_a_eliminar in integrantes_a_eliminar:
        integrante_a_eliminar.fecha_baja = timezone.now()
        integrante_a_eliminar.save()
    # Agregar nuevos integrantes
    for integrante in estudiantes_seleccionados:
        if integrante not in estudiantes_actuales:
            nuevosIntegrantes.append(integrante.id)

    agregarIntegranteProyecto(nuevosIntegrantes, proyecto)

def modificarRolProyecto(director_seleccionado, codirector_seleccionado, proyecto):
    print (director_seleccionado)
    roles_actuales = proyecto.proyecto.all()
    for rol_actual in roles_actuales:
        if rol_actual.descripcion == 'Director':
            # Verifica si el director seleccionado coincide con el rol actual
            if rol_actual.docente.id == int(director_seleccionado):
                pass
            else:
                # Establece la fecha de baja para el Director actual y agrega un nuevo Director
                rol_actual.fecha_baja = timezone.now()
                rol_actual.save()
                agregarRolProyecto(director_seleccionado, proyecto, 'Director')
        else:
            if rol_actual.docente.id == int(codirector_seleccionado):
                pass
            else:
                # Establece la fecha de baja para el Codirector actual y agrega un nuevo Codirector
                rol_actual.fecha_baja = timezone.now()
                rol_actual.save()
                agregarRolProyecto(codirector_seleccionado, proyecto, 'Codirector')

def modificarAsesorProyecto(asesor_seleccionado, proyecto):
    asesor_actual_list = proyecto.asesor_proyecto.all()
    for asesor_actual in asesor_actual_list:
        if asesor_actual.asesor.id == asesor_seleccionado:
            pass
        else:
            asesor_actual.asesor = Asesor.objects.get(id=asesor_seleccionado)
            asesor_actual.save()

def modificarCSTFProyecto(comision_seleccionada, proyecto):
    comision_actual = proyecto.comision_proyecto
    if comision_actual.comision.id == comision_seleccionada:
        pass
    else:
        comision_actual.comision = Comision.objects.get(id=comision_seleccionada)
        comision_actual.fecha_alta = timezone.now()
        comision_actual.save()
@login_required
def proyecto_integrante_edit(request, id):
    proyecto = Proyecto.objects.get(id=id)

    if request.method == 'POST':
        integrantes_seleccionados = request.POST.getlist('integrantesSelecionados')
        asesor_seleccionado = request.POST.get('asesor_seleccionado')
        director_seleccionado = request.POST.get('director_seleccionado')
        codirector_seleccionado = request.POST.get('codirector_seleccionado')
        comision_seleccionada = request.POST.get('comision_seleccionada')
        if integrantes_seleccionados and asesor_seleccionado and director_seleccionado and codirector_seleccionado:
            modificarIntegranteProyecto(integrantes_seleccionados, proyecto)
            modificarRolProyecto(director_seleccionado, codirector_seleccionado, proyecto)
            modificarAsesorProyecto(asesor_seleccionado, proyecto)
            modificarCSTFProyecto(comision_seleccionada, proyecto)
            messages.success(request, 'Se ha actualizado correctamente los integrantes del Proyecto')
            return redirect(reverse('gestion:detalle_proyecto', args=[proyecto.id]))

    estudiantes, estudiantes_selecionados, docentes, director, codirector, asesores, asesor, comisiones, comision = obtenerIntegrantes(
        proyecto)

    return render(request, 'proyectos/proyecto_integrante_edit.html', {'estudiantes': estudiantes,
                                                                       'estudiantes_selecionados': estudiantes_selecionados,
                                                                       'docentes': docentes,
                                                                       'director': director.docente,
                                                                       'codirector': codirector.docente,
                                                                       'asesores': asesores,
                                                                       'asesor_seleccionado': asesor.asesor,
                                                                       'comisiones': comisiones,
                                                                       'comision_seleccionada': comision})

@login_required
@user_passes_test(es_departamento)
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

            messages.success(request, 'Se ha creado el proyecto correctamente. Asigne un tribunal para el mismo.')
            # return redirect(reverse('gestion:detalle_proyecto', args={proyecto_instance.id}))
            # return redirect('gestion:detalle_proyecto', proyecto_instance.id)
            return redirect('gestion:nuevo_tribunal', proyecto_instance.id)
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


@user_passes_test(es_movimientos)
def cargarNuevoPTF(request, id):
    proyecto = get_object_or_404(Proyecto, id=id)
    ultimo_estado = proyecto.proyecto_instancia.last()
    ultima_evaluacion = ultimo_estado.instancia_evaluacion.last()
    nuevo_adjunto = request.FILES['nuevoPTF']
    if nuevo_adjunto:
        nombre_original = nuevo_adjunto.name
        nombre_base, extension = os.path.splitext(nombre_original)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        nombre_archivo = f"{nombre_base}_{timestamp}{extension}"

        with open(f'media/uploads/{nombre_archivo}', 'wb') as destination:
            for chunk in nuevo_adjunto.chunks():
                destination.write(chunk)

        # Ahora puedes asignar el archivo adjunto a otro objeto si es necesario
        ultima_evaluacion.nuevoPTF = nuevo_adjunto
        ultima_evaluacion.save()
        return redirect(reverse('gestion:movimientos', args=[proyecto.id]))
        # return render(request, 'movimientos/movimientos.html', {'proyecto': proyecto})


def habilitarDefensa(proyecto):
    ultimo_estado = proyecto.proyecto_instancia.last()
    if ultimo_estado.descripcion == 'FINALIZADO':
        estados_anteriores = proyecto.proyecto_instancia.exclude(id=ultimo_estado.id).order_by('-id')
        if estados_anteriores.exists():
            estado_anterior = estados_anteriores.first()
            ultima_evaluacion = estado_anterior.instancia_evaluacion.last()
            if ultima_evaluacion and ultima_evaluacion.estado == 'APROBADO':
                return True

    return False


def habilitarEvaluacion(proyecto):
    ultimo_estado = proyecto.proyecto_instancia.last()
    ultima_evaluacion = ultimo_estado.instancia_evaluacion.last()
    if ultimo_estado.descripcion == 'FINALIZADO':
        return False
    elif ultima_evaluacion is None:
        # if ultimo_estado.descripcion == 'COMISION DE SEGUIMIENTO':
        return True
    elif ultima_evaluacion.estado == 'OBSERVADO' and not ultima_evaluacion.nuevoPTF:
        return False
    else:
        return True


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


@user_passes_test(es_movimientos)
def movimientos(request, id):
    proyecto = get_object_or_404(Proyecto, id=id)
    if request.method == 'POST':
        form_evaluacion = EvaluacionForm(request.POST, request.FILES, prefix='evaluacion')
        form_defensa = DefensaForm(request.POST, request.FILES, prefix='defensa')
        instancia_actual = proyecto.proyecto_instancia.last()

        if form_evaluacion.is_valid():
            evaluacion_instance = form_evaluacion.save(commit=False)
            evaluacion_instance.fecha = timezone.now()
            evaluacion_instance.instancia_evaluacion = instancia_actual
            evaluacion_instance.save()
            controlEstado(proyecto.id)
            return redirect(reverse('gestion:movimientos', args={proyecto.id}))

        elif form_defensa.is_valid():
            defensa_instance = form_defensa.save(commit=False)
            defensa_instance.proyecto = proyecto
            defensa_instance.save()
            return redirect(reverse('gestion:movimientos', args={proyecto.id}))

    else:
        form_evaluacion = EvaluacionForm(prefix='evaluacion')
        form_defensa = DefensaForm(prefix='defensa')

    habilitar_defensa = habilitarDefensa(proyecto)
    habilitar_evaluacion = habilitarEvaluacion(proyecto)
    return render(request, 'movimientos/movimientos.html', {
        'proyecto': proyecto,
        'form_evaluacion': form_evaluacion,
        'form_defensa': form_defensa,
        'habilitar_defensa': habilitar_defensa,
        'habilitar_evaluacion': habilitar_evaluacion})


def seccionComision(request):
    comisiones = Comision.objects.all()
    return render(request, 'comision/comision_seguimiento.html', {'comisiones': comisiones})


def agregarIntegranteComision(integrantes, comision):
    docentes_seleccionados = Docente.objects.filter(id__in=integrantes)
    for integrante in docentes_seleccionados:
        integrante_comision_instance = IntegranteComision(comision=comision,
                                                          docente=integrante,
                                                          fecha_alta=timezone.now())
        integrante_comision_instance.save()

def actualizarIntegrantesComision(integrantesSelec, comision, integrantes):
    docentes_seleccionados = Docente.objects.filter(id__in=integrantesSelec)
    docentes_integrantes = []
    for i in integrantes:
        docentes_integrantes.append(i.docente)

    for integrante in docentes_seleccionados:
        if integrante not in docentes_integrantes:
            integrante_comision_instance = IntegranteComision(comision=comision,
                                                              docente=integrante,
                                                              fecha_alta=timezone.now())
            integrante_comision_instance.save()

    for integrante in integrantes:
        docente = integrante.docente
        if docente not in docentes_seleccionados:
            integrante_baja = IntegranteComision.objects.filter(comision=comision, docente=docente)
            for integ in integrante_baja:
                integ.delete()

@user_passes_test(es_departamento)
def nuevaComision(request):
    if request.method == 'POST':
        form_comision = ComisionForm(request.POST, request.FILES)
        integrantes_seleccionados = request.POST.getlist('integrantesSelecionados')
        if form_comision.is_valid() and integrantes_seleccionados:
            comision_instance = form_comision.save()
            agregarIntegranteComision(integrantes_seleccionados, comision_instance)
            asignarUsuariosGrupo(integrantes_seleccionados, 'Comision de Seguimiento')

            messages.success(request, 'Se ha creado la comisión correctamente.')
            return redirect('gestion:detalle_integrantes_comision', comision_instance.id)

    else:
        form_comision = ComisionForm()

    docentes = Docente.objects.all()
    return render(request, 'comision/registro_CSTF.html', {
        'form_comision': form_comision,
        'docentes': docentes,
    })


def detalleIntegrantesComision(request, id):
    comision = get_object_or_404(Comision, id=id)
    return render(request, 'comision/detalleIntegrantes.html', {'comision': comision})

def comision_edit(request, id):
    comision = get_object_or_404(Comision, id=id)
    integrantes = IntegranteComision.objects.filter(comision=comision)
    if request.method == 'POST':
        form_comision = ComisionForm(request.POST, request.FILES, instance=comision)
        integrantes_seleccionados = request.POST.getlist('integrantesSelecionados')
        if form_comision.is_valid() and integrantes_seleccionados:
            comision_instance = form_comision.save()
            actualizarIntegrantesComision(integrantes_seleccionados, comision_instance, integrantes)
            messages.success(request, 'Se ha actualizado correctamente la comisión')
            return redirect(reverse('gestion:detalle_integrantes_comision', args=[comision_instance.id]))
    else:
        form_comision = ComisionForm(instance=comision)
    docentes = Docente.objects.all()
    return render(request, 'comision/comision_edit.html', {
        'form_comision': form_comision,
        'docentes': docentes,
        'integrantes': integrantes,
        'comision': comision,
    })

def detalleProyectosComision(request, id):
    comision = get_object_or_404(Comision, id=id)
    return render(request, 'comision/detalleProyectos.html', {'comision': comision})


def seccionTribunales(request):
    tribunales = Tribunal.objects.all().order_by('-fecha_disposicion')
    return render(request, 'tribunales/tribunales.html', {'tribunales': tribunales})


def detalleIntegrantesTribunal(request, id):
    tribunal = get_object_or_404(Tribunal, id=id)
    return render(request, 'tribunales/detalleIntegrantes.html', {'tribunal': tribunal})


def detalleProyectosTribunal(request, id):
    tribunal = get_object_or_404(Tribunal, id=id)
    return render(request, 'tribunales/detalleProyectos.html', {'tribunal': tribunal})


def agregarIntegrantesTribunal(integrantes, tribunal, rol):
    docentes_seleccionados = Docente.objects.filter(id__in=integrantes)
    for integrante in docentes_seleccionados:
        integrante_tribunal_instance = RolTribunal(descripcion=rol,
                                                   tribunal=tribunal,
                                                   docente=integrante,
                                                   fecha_alta=timezone.now())
        integrante_tribunal_instance.save()


@user_passes_test(es_departamento)
def nuevoTribunal(request, id):
    if request.method == 'POST':
        form_tribunal = TribunalForm(request.POST, request.FILES, prefix='tribunal')
        presidente_seleccionado = request.POST.getlist('presidente_seleccionado')
        vocales_seleccionados = request.POST.getlist('vocales_seleccionados')
        vocales_suplentes_seleccionados = request.POST.getlist('vocales_suplentes_seleccionados')
        if form_tribunal.is_valid() and presidente_seleccionado and vocales_seleccionados and vocales_suplentes_seleccionados:
            tribunal_instance = form_tribunal.save(commit=False)
            tribunal_instance.proyecto = get_object_or_404(Proyecto, id=id)
            tribunal_instance.save()
            agregarIntegrantesTribunal(presidente_seleccionado, tribunal_instance, 'Presidente')
            agregarIntegrantesTribunal(vocales_seleccionados, tribunal_instance, 'Vocal')
            agregarIntegrantesTribunal(vocales_suplentes_seleccionados, tribunal_instance, 'Vocal suplente')
            asignarUsuariosGrupo(presidente_seleccionado, 'Tribunal')
            asignarUsuariosGrupo(vocales_seleccionados, 'Tribunal')
            asignarUsuariosGrupo(vocales_seleccionados, 'Tribunal')

            messages.success(request, 'Se ha asignado el tribunal al pryecto correctamente.')
            return redirect('gestion:detalle_proyecto', id)
    else:
        form_tribunal = TribunalForm(prefix='tribunal')

    docentes = Docente.objects.all()
    return render(request, 'tribunales/registro.html', {
        'form_tribunal': form_tribunal,
        'docentes': docentes})
