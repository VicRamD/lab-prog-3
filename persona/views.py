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
            return redirect(reverse('persona:detalle_estudiante', args={estudiante_instance.id}))
    else:
        form_persona = EstudianteForm()

    return render(request, 'formulario_creacion.html', {'form_persona': form_persona,
                                                        'tipo_persona':'estudiante'})

def estudianteDetalle(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)
    return render(request, 'detalle_persona.html',
                  {'persona': estudiante, 'tipo_persona': 'estudiante'})