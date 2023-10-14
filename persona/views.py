from django.shortcuts import render, get_object_or_404, redirect

from persona.forms import EstudianteForm, AsesorForm, DocenteForm


# Create your views here.

def nuevoEstudiante(request):
    if request.method == 'POST':
        form_estudiante = EstudianteForm(request.POST, request.FILES)
        if form_estudiante.is_valid():
            estudiante_instance = form_estudiante.save()
            return redirect('persona:detalle_estudiante', estudiante_instance.id)
    else:
        form_persona = EstudianteForm()

    return render(request, 'formulario_creacion.html', {'form_persona': form_persona,
                                                        'tipo_persona':'estudiante'})