from django.shortcuts import render, get_object_or_404, redirect

from persona.forms import EstudianteForm, AsesorForm, DocenteForm
from django.urls import reverse
from django.contrib import messages

from persona.models import Estudiante, Asesor, Docente
# Create your views here.

def nuevoEstudiante(request):
    if request.method == 'POST':
        form_persona = EstudianteForm(request.POST, request.FILES)
        if form_persona.is_valid():
            estudiante_instance = form_persona.save()
            estudiante_instance.guardar_dni()
            estudiante_instance.save()
            messages.success(request, 'Datos de estudiante guardados correctamente')
            return redirect(reverse('persona:detalle_estudiante', args={estudiante_instance.id}))
        else:
            datos = request.POST.dict()
            cuil = datos.get("cuil")
            mensajeErrorCuil(request, cuil)
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

def nuevoAsesor(request):
    if request.method == 'POST':
        form_persona = AsesorForm(request.POST, request.FILES)
        if form_persona.is_valid():
            asesor_instance = form_persona.save()
            asesor_instance.guardar_dni()
            asesor_instance.save()
            messages.success(request, 'Datos de asesor guardados correctamente')
            return redirect(reverse('persona:detalle_asesor', args={asesor_instance.id}))
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

def nuevoDocente(request):
    if request.method == 'POST':
        form_persona = DocenteForm(request.POST, request.FILES)
        if form_persona.is_valid():
            docente_instance = form_persona.save()
            docente_instance.guardar_dni()
            docente_instance.save()
            messages.success(request, 'Datos de docente guardados correctamente')
            return redirect(reverse('persona:detalle_docente', args={docente_instance.id}))
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