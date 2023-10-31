from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, get_object_or_404, redirect

from persona.forms import EstudianteForm, AsesorForm, DocenteForm, EstudianteUpdateForm, AsesorUpdateForm, DocenteUpdateForm
from django.urls import reverse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

from persona.models import Estudiante, Asesor, Docente, IntegranteProyecto, RolProyecto, AsesorProyecto
from usuarios.models import Usuario_persona
from gestion.models import Proyecto
# Create your views here.

def buscarStringEnCuil(tipo, cuil):
    listas_devueltas = []
    if tipo == 'estudiantes':
        l_busqueda = Estudiante.objects.filter(cuil__icontains=cuil)
        listas_devueltas.append(l_busqueda)
    elif tipo == 'docentes':
        l_busqueda = Docente.objects.filter(cuil__icontains=cuil)
        listas_devueltas.append(l_busqueda)
    elif tipo == 'asesores':
        l_busqueda = Asesor.objects.filter(cuil__icontains=cuil)
        listas_devueltas.append(l_busqueda)
    else:
        lb_estudiantes = Estudiante.objects.filter(cuil__icontains=cuil)
        lb_docentes = Docente.objects.filter(cuil__icontains=cuil)
        lb_asesores = Asesor.objects.filter(cuil__icontains=cuil)
        listas_devueltas.append(lb_estudiantes)
        listas_devueltas.append(lb_docentes)
        listas_devueltas.append(lb_asesores)
    return listas_devueltas

def listadoPersonas(request):
    estudiantes = Estudiante.objects.all().order_by('apellido', 'nombre')
    docentes = Docente.objects.all().order_by('apellido', 'nombre')
    asesores = Asesor.objects.all().order_by('apellido', 'nombre')
    if request.method == 'POST':
        tipo_seleccionado = request.POST.get('tipo_seleccionado')
        cuil_buscado = request.POST.get('cuil_buscado')
        estudiantes_lista = estudiantes
        docentes_lista = docentes
        asesores_lista = asesores
        #listas = []
        if tipo_seleccionado != 'TODOS' and cuil_buscado:
            if tipo_seleccionado == 'ESTUDIANTES':
                estudiantes_cuil = buscarStringEnCuil('estudiantes', cuil_buscado)
                return render(request, 'personas_registradas.html', {'estudiantes': estudiantes_cuil[0]})
            if tipo_seleccionado == 'DOCENTES':
                #listas.append(docentes_lista)
                docentes_cuil = buscarStringEnCuil('docentes', cuil_buscado)
                return render(request, 'personas_registradas.html', {'docentes': docentes_cuil[0]})
            if tipo_seleccionado == 'ASESORES':
                asesores_cuil = buscarStringEnCuil('asesores', cuil_buscado)
                return render(request, 'personas_registradas.html', {'asesores': asesores_cuil[0]})
        elif cuil_buscado:
            #print("En elif cuil buscado")
            # listas.append(estudiantes_lista)
            # listas.append(docentes_lista)
            # listas.append(asesores_lista)
            lista_registros_cuil = buscarStringEnCuil('todos', cuil_buscado)
            return render(request, 'personas_registradas.html', {'estudiantes': lista_registros_cuil[0],
                                                                 'docentes': lista_registros_cuil[1],
                                                                 'asesores': lista_registros_cuil[2]
                                                                 })
        elif tipo_seleccionado != 'TODOS':
            if tipo_seleccionado == 'ESTUDIANTES':
                return render(request, 'personas_registradas.html', {'estudiantes': estudiantes_lista})
            if tipo_seleccionado == 'DOCENTES':
                return render(request, 'personas_registradas.html', {'docentes': docentes_lista})
            if tipo_seleccionado == 'ASESORES':
                return render(request, 'personas_registradas.html', {'asesores': asesores_lista})
        else:
            return render(request, 'personas_registradas.html', {'estudiantes': estudiantes,
                                                                 'docentes': docentes,
                                                                 'asesores': asesores
                                                                 })
    else:
        return render(request, 'personas_registradas.html', {'estudiantes': estudiantes,
                                                                 'docentes': docentes,
                                                                 'asesores': asesores
                                                                 })

# ============== Estudiante =================================
def nuevoEstudiante(request):
    if request.method == 'POST':
        form_persona = EstudianteForm(request.POST, request.FILES)
        if form_persona.is_valid():
            estudiante_instance = form_persona.save()
            estudiante_instance.guardar_dni()
            estudiante_instance.save()
            messages.success(request, 'Datos de estudiante guardados correctamente')
            #return redirect(reverse('persona:detalle_estudiante', args={estudiante_instance.id}))
            return redirect(reverse('usuarios:registrar_usuario', kwargs={'id': estudiante_instance.id, 'grupo': 'Estudiante'}))
        else:
            datos = request.POST.dict()
            cuil = datos.get("cuil")
            matricula = datos.get("matricula")
            email = datos.get("email")
            mensajeErrorCuil(request, cuil)
            mensajeErrorMatricula(request, matricula)
            mensajeErrorEmail(request, email)
            diccionario = datosEnDiccionario(datos)
            return render(request, 'formulario_creacion.html', {'form_persona': form_persona,
                                                        'tipo_persona': 'estudiante',
                                                                'campos': diccionario,
                                                                })

    else:
        form_persona = EstudianteForm()
    #estudiantes_registrados = Estudiante.objects.all()
    return render(request, 'formulario_creacion.html', {'form_persona': form_persona,
                                                        'tipo_persona': 'estudiante'})

def estudianteDetalle(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)
    return render(request, 'detalle_persona.html',
                  {'persona': estudiante, 'tipo_persona': 'estudiante'})

def estudianteModificar(request, pk):
    estudiante_revisado = Estudiante.objects.get(id=pk)
    estudiante = get_object_or_404(Estudiante, pk=pk)
    if request.method == 'POST':
        form_persona = EstudianteUpdateForm(request.POST, request.FILES, instance=estudiante)
        print(form_persona.is_valid())
        if form_persona.is_valid():
            form_persona.save()
            messages.success(request, 'Se ha actualizado correctamente los datos del estudiante')
            return redirect(reverse('persona:detalle_estudiante', args=[estudiante.id]))
    else:
        form_persona = EstudianteUpdateForm(instance=estudiante)
    return render(request, 'formulario_edicion_persona.html', {'form_persona': form_persona,
                                                           'tipo_persona': 'estudiante',
                                                               'persona': estudiante_revisado})

def estudianteEliminar(request):
    if request.method == 'POST':
        if 'id_persona' in request.POST:
            estudiante = get_object_or_404(Estudiante, pk=request.POST['id_persona'])
            nombre_estudiante = estudiante.nombre_completo()
            estudiante.delete()
            messages.success(request, 'Se ha eliminado exitosamente al estudiante: {}'.format(nombre_estudiante))
        else:
            messages.error(request, 'Debe indicar qué Estudiante se desea eliminar')
    return redirect(reverse('persona:lista_personas'))

#========================================================
# ============== Asesor =================================
@login_required(login_url='usuarios:login')
@permission_required('asesor.add_asesor', raise_exception=True)
def nuevoAsesor(request):
    if request.method == 'POST':
        form_persona = AsesorForm(request.POST, request.FILES)
        if form_persona.is_valid():
            asesor_instance = form_persona.save()
            asesor_instance.guardar_dni()
            asesor_instance.save()
            messages.success(request, 'Datos de asesor guardados correctamente')
            #return redirect(reverse('persona:detalle_asesor', args={asesor_instance.id}))
            return redirect(reverse('usuarios:registrar_usuario', kwargs={'id': asesor_instance.id, 'grupo': 'Asesor'}))
        else:
            datos = request.POST.dict()
            archivos = request.FILES.dict()
            cuil = datos.get("cuil")
            cv = archivos.get("cv")
            mensajeErrorCuil(request, cuil)
            mensajeExtensionCV(request, cv)
            diccionario = datosEnDiccionario(datos)
            return render(request, 'formulario_creacion.html', {'form_persona': form_persona,
                                                                'tipo_persona': 'asesor',
                                                                'campos': diccionario,
                                                                })
    else:
        form_persona = AsesorForm()

    return render(request, 'formulario_creacion.html', {'form_persona': form_persona,
                                                        'tipo_persona': 'asesor'})

def asesorDetalle(request, pk):
    asesor = get_object_or_404(Asesor, pk=pk)
    return render(request, 'detalle_persona.html',
                  {'persona': asesor, 'tipo_persona': 'asesor'})

def asesorModificar(request, pk):
    asesorDetalle_revisado = Asesor.objects.get(id=pk)
    asesor = get_object_or_404(Asesor, pk=pk)
    if request.method == 'POST':
        form_persona = AsesorUpdateForm(request.POST, request.FILES, instance=asesor)
        if form_persona.is_valid():
            form_persona.save()
            messages.success(request, 'Se ha actualizado correctamente los datos del asesor')
            return redirect(reverse('persona:detalle_asesor', args=[asesor.id]))
    else:
        form_persona = AsesorUpdateForm(instance=asesor)
    return render(request, 'formulario_edicion_persona.html', {'form_persona': form_persona,
                                                           'tipo_persona': 'asesor',
                                                               'persona': asesorDetalle_revisado})

def asesorEliminar(request):
    if request.method == 'POST':
        if 'id_persona' in request.POST:
            asesor = get_object_or_404(Asesor, pk=request.POST['id_persona'])
            nombre_asesor = asesor.nombre_completo()
            asesor.delete()
            messages.success(request, 'Se ha eliminado exitosamente al asesor: {}'.format(nombre_asesor))
        else:
            messages.error(request, 'Debe indicar qué Asesor se desea eliminar')
    return redirect(reverse('persona:lista_personas'))

#========================================================
# ============== Docente =================================
def nuevoDocente(request):
    if request.method == 'POST':
        form_persona = DocenteForm(request.POST, request.FILES)
        if form_persona.is_valid():
            docente_instance = form_persona.save()
            docente_instance.guardar_dni()
            docente_instance.save()
            messages.success(request, 'Datos de docente guardados correctamente')
            #return redirect(reverse('persona:detalle_docente', args={docente_instance.id}))
            return redirect(reverse('usuarios:registrar_usuario', kwargs={'id': docente_instance.id, 'grupo': 'Docente'}))
        else:
            datos = request.POST.dict()
            cuil = datos.get("cuil")
            mensajeErrorCuil(request, cuil)
            diccionario = datosEnDiccionario(datos)
            return render(request, 'formulario_creacion.html', {'form_persona': form_persona,
                                                                'tipo_persona': 'docente',
                                                                'campos': diccionario,
                                                                })
    else:
        form_persona = DocenteForm()

    return render(request, 'formulario_creacion.html', {'form_persona': form_persona,
                                                        'tipo_persona': 'docente'})

def docenteDetalle(request, pk):
    docente = get_object_or_404(Docente, pk=pk)
    return render(request, 'detalle_persona.html',
                  {'persona': docente, 'tipo_persona': 'docente'})

def docenteModificar(request, pk):
    docente_revisado = Docente.objects.get(id=pk)
    docente = get_object_or_404(Docente, pk=pk)
    if request.method == 'POST':
        form_persona = DocenteUpdateForm(request.POST, request.FILES, instance=docente)
        if form_persona.is_valid():
            form_persona.save()
            messages.success(request, 'Se ha actualizado correctamente los datos del docente')
            return redirect(reverse('persona:detalle_docente', args=[docente.id]))
    else:
        form_persona = DocenteUpdateForm(instance=docente)
    return render(request, 'formulario_edicion_persona.html', {'form_persona': form_persona,
                                                           'tipo_persona': 'docente',
                                                               'persona': docente_revisado})

def docenteEliminar(request):
    if request.method == 'POST':
        if 'id_persona' in request.POST:
            docente = get_object_or_404(Docente, pk=request.POST['id_persona'])
            nombre_docente = docente.nombre_completo()
            docente.delete()
            messages.success(request, 'Se ha eliminado exitosamente al docente: {}'.format(nombre_docente))
        else:
            messages.error(request, 'Debe indicar qué Docente se desea eliminar')
    return redirect(reverse('persona:lista_personas'))

#========================================================
#=========================================================
def listado_proyectos(request):
    current_user = request.user
    if request.user.is_authenticated:
        relacion = Usuario_persona.objects.get(user=current_user)
        if relacion.tipo == "estudiante":
            persona = relacion.estudiante
            proyectos_que_integra = IntegranteProyecto.objects.filter(estudiante=persona)
            proyectos_lista = proyectos_devolver(proyectos_que_integra)
        elif relacion.tipo == "docente":
            persona = relacion.docente
            proyectos_que_integra = RolProyecto.objects.filter(docente=persona)
            proyectos_lista = proyectos_devolver(proyectos_que_integra)
        else:
            persona = relacion.asesor
            proyectos_que_integra = AsesorProyecto.objects.filter(asesor=persona)
            proyectos_lista = proyectos_devolver(proyectos_que_integra)

        return render(request, 'con_sesion/ptf_relacionados_cuenta.html', {
            'persona': persona,
            'tipo_persona': relacion.tipo,
            'proyectos_lista': proyectos_lista,
        })

def estado_proyecto(request, pk):
    current_user = request.user
    if request.user.is_authenticated:
        proyecto = Proyecto.objects.get(id=pk)
        relacion = Usuario_persona.objects.get(user=current_user)
        if relacion.tipo == "estudiante":
            persona = relacion.estudiante
        elif relacion.tipo == "docente":
            persona = relacion.docente
        else:
            persona = relacion.asesor

        return render(request, 'con_sesion/ptf_estado_proyecto.html', {
                                                        'persona': persona,
                                                        'proyecto': proyecto,
                                                        'tipo_persona': relacion.tipo,
                                                        })

#========================================================
#Funciones para ser usadas
def mensajeErrorCuil(request, cuil):
    estudiantes_con_cuil = Estudiante.objects.filter(cuil=cuil)
    if estudiantes_con_cuil.count() != 0:
        mensaje = "Hay un estudiante registrado con el cuil " + cuil + ": "  + estudiantes_con_cuil[0].nombre_completo()
        messages.error(request, mensaje)
        #return mensaje
    docentes_con_cuil = Docente.objects.filter(cuil=cuil)
    if docentes_con_cuil.count() != 0:
        mensaje = "Hay un docente registrado con el cuil " + cuil + ": "  + estudiantes_con_cuil[0].nombre_completo()
        messages.error(request, mensaje)
        #return mensaje
    asesores_con_cuil = Asesor.objects.filter(cuil=cuil)
    if asesores_con_cuil.count() != 0:
        mensaje = "Hay un asesor registrado con el cuil " + cuil + ": "  + estudiantes_con_cuil[0].nombre_completo()
        messages.error(request, mensaje)
        #return mensaje

def mensajeErrorMatricula(request, matricula):
    estudiantes_con_matricula = Estudiante.objects.filter(matricula=matricula)
    if estudiantes_con_matricula.count() != 0:
        mensaje = "Hay un estudiante registrado con el cuil " + matricula + ": " + estudiantes_con_matricula[0].nombre_completo()
        messages.error(request, mensaje)

def mensajeErrorEmail(request, email):
    estudiantes_con_email = Estudiante.objects.filter(email=email)
    if estudiantes_con_email.count() != 0:
        mensaje = "Hay un estudiante registrado con el cuil " + email + ": " + estudiantes_con_email[0].nombre_completo()
        messages.error(request, mensaje)
        #return mensaje
    docentes_con_email = Docente.objects.filter(email=email)
    if docentes_con_email.count() != 0:
        mensaje = "Hay un docente registrado con el cuil " + email + ": " + docentes_con_email[0].nombre_completo()
        messages.error(request, mensaje)
        #return mensaje
    asesores_con_email = Asesor.objects.filter(email=email)
    if asesores_con_email.count() != 0:
        mensaje = "Hay un asesor registrado con el cuil " + email + ": " + asesores_con_email[0].nombre_completo()
        messages.error(request, mensaje)
        #return mensaje

def datosEnDiccionario(datos):
    nombre = datos.get("nombre")
    apellido = datos.get("apellido")
    cuil = datos.get("cuil")
    telefono = datos.get("telefono")
    email = datos.get("email")
    data = {
        'nombre': nombre,
        'apellido': apellido,
        'cuil': cuil,
        'telefono': telefono,
        'email': email,
    }
    return data

def mensajeExtensionCV(request, cv):
    if cv:
        extension = cv.name.rsplit('.', 1)[1].lower()
        if extension != 'pdf':
            messages.error(request, 'El archivo seleccionado no tiene el formato PDF.')

def proyectos_devolver(proyectos_que_integra):
    proyectos_lista = []
    for proyecto in proyectos_que_integra:
        proyectos_lista.append(proyecto.proyecto)
    return proyectos_lista