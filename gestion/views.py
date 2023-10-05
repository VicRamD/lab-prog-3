#from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def seccionProyectos(request):
    return render(request, 'proyectos/proyectos.html')

def nuevoProyecto(request):
    return render(request, 'proyectos/nuevo_proyecto.html')

def estadisticas(request):
    return render(request, 'proyectos/eProyectos.html')
