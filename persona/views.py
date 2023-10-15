from django.shortcuts import render, get_object_or_404, redirect

from persona.forms import EstudianteForm, AsesorForm, DocenteForm
from django.urls import reverse

from persona.models import Estudiante, Asesor, Docente
# Create your views here.

def nuevoEstudiante(request):
    if request.method == 'POST':
        form_estudiante = EstudianteForm(request.POST, request.FILES)
        if form_estudiante.is_valid():
            estudiante_instance = form_estudiante.save()
            estudiante_instance.guardar_dni()
            estudiante_instance.save()
            return redirect(reverse('persona:detalle_estudiante', args={estudiante_instance.id}))
    else:
        form_persona = EstudianteForm()

    return render(request, 'formulario_creacion.html', {'form_persona': form_persona,
                                                        'tipo_persona': 'estudiante'})

def estudianteDetalle(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)
    return render(request, 'detalle_persona.html',
                  {'persona': estudiante, 'tipo_persona': 'estudiante'})

def nuevoAsesor(request):
    if request.method == 'POST':
        form_asesor = AsesorForm(request.POST, request.FILES)
        if form_asesor.is_valid():
            asesor_instance = form_asesor.save()
            asesor_instance.guardar_dni()
            asesor_instance.save()
            return redirect(reverse('persona:detalle_asesor', args={asesor_instance.id}))
    else:
        form_persona = AsesorForm()

    return render(request, 'formulario_creacion.html', {'form_persona': form_persona,
                                                        'tipo_persona': 'asesor'})

def asesorDetalle(request, pk):
    asesor = get_object_or_404(Estudiante, pk=pk)
    return render(request, 'detalle_persona.html',
                  {'persona': asesor, 'tipo_persona': 'asesor'})

def nuevoDocente(request):
    if request.method == 'POST':
        form_docente = DocenteForm(request.POST, request.FILES)
        if form_docente.is_valid():
            docente_instance = form_docente.save()
            docente_instance.guardar_dni()
            docente_instance.save()
            return redirect(reverse('persona:detalle_docente', args={docente_instance.id}))
    else:
        form_persona = DocenteForm()

    return render(request, 'formulario_creacion.html', {'form_persona': form_persona,
                                                        'tipo_persona':'docente'})

def docenteDetalle(request, pk):
    docente = get_object_or_404(Estudiante, pk=pk)
    return render(request, 'detalle_persona.html',
                  {'persona': docente, 'tipo_persona': 'docente'})

