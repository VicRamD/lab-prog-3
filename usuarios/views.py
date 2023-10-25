from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .forms import CrearUsuarioForm
from persona.models import Estudiante, Docente, Asesor


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("usuarios:login"))
    return render(request, "index.html")


def login_view(request):
    if request.method == "POST":
        usuario = request.POST["usuario"]
        password = request.POST["password"]
        user = authenticate(request, username=usuario, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("usuarios:index"))
        else:
            return render(request, "index.html", {"mensaje": "Los datos son incorrectos"})
    return render(request, 'index.html')


def logout_view(request):
    logout(request)
    return render(request, "index.html", {"mensaje": "Sesión finalizada"})


def registrar_usuario(request, id, grupo):
    data = {
        'form': CrearUsuarioForm()
    }
    if grupo == 'Estudiante':
        persona = get_object_or_404(Estudiante, id=id)
    elif grupo == 'Docente':
        persona = get_object_or_404(Docente, id=id)
    else:
        persona = get_object_or_404(Asesor, id=id)

    if request.method == 'POST':
        user_creation_form = CrearUsuarioForm(data=request.POST)

        if user_creation_form.is_valid():
            usuario_instance = user_creation_form.save(commit=False)
            usuario_instance.first_name = persona.nombre
            usuario_instance.last_name = persona.apellido
            usuario_instance.email = persona.email
            usuario_instance.save()
            # Asignar al usuario el grupo correspondiente
            if grupo == 'Estudiante':
                estudiante_group = Group.objects.get(name='Estudiante')
                usuario_instance.groups.add(estudiante_group)
            elif grupo == 'Docente':
                docente_group = Group.objects.get(name='Docente')
                usuario_instance.groups.add(docente_group)
            else:
                asesor_group = Group.objects.get(name='Asesor')
                usuario_instance.groups.add(asesor_group)

            return redirect('persona:lista_personas')
        else:
            data['form'] = user_creation_form

    return render(request, 'registro_usuario.html', data)
