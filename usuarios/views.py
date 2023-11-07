from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .forms import CrearUsuarioForm
from persona.models import Estudiante, Docente, Asesor
from django.contrib.auth.models import User
from usuarios.models import Usuario_persona


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("usuarios:login"))
    '''
    usuario_grupo = request.user.groups.filter(name='Departamento Academico').exists()
    context = {
        'usuario_grupo': usuario_grupo
    }'''
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


def obtenerPersona(id, grupo):
    if grupo == 'Estudiante':
        persona = get_object_or_404(Estudiante, id=id)
    elif grupo == 'Docente':
        persona = get_object_or_404(Docente, id=id)
    else:
        persona = get_object_or_404(Asesor, id=id)
    return persona


def asignarUsuariosGrupo(docentes, grupo):
    listado_docente = Docente.objects.filter(id__in=docentes)
    mails_docentes = []
    for docente in listado_docente:
        mails_docentes.append(docente.email)
    listado_usuarios = User.objects.filter(email__in=mails_docentes)
    for usuario in listado_usuarios:
        if not usuario.groups.filter(name=grupo).exists():
            usuario_group = Group.objects.get(name=grupo)
            print(usuario.groups.name)
            usuario.groups.add(usuario_group)
            usuario.save()


def registrar_usuario(request, id, grupo):
    data = {
        'form': CrearUsuarioForm()
    }

    if request.method == 'POST':
        user_creation_form = CrearUsuarioForm(data=request.POST)

        if user_creation_form.is_valid():
            usuario_instance = user_creation_form.save(commit=False)
            persona = obtenerPersona(id, grupo)
            usuario_instance.first_name = persona.nombre
            usuario_instance.last_name = persona.apellido
            usuario_instance.email = persona.email
            usuario_instance.save()
            enlace_usuario_persona(usuario_instance, persona, grupo)
            usuario_group = Group.objects.get(name=grupo)
            usuario_instance.groups.add(usuario_group)
            return redirect('persona:lista_personas')
        else:
            data['form'] = user_creation_form

    return render(request, 'registro_usuario.html', data)


def es_estudiante(user):
    return user.groups.filter(name='Estudiante').exists()


def es_docente(user):
    return user.groups.filter(name='Docente').exists()


def es_asesor(user):
    return user.groups.filter(name='Asesor').exists()


def es_comision(user):
    return user.groups.filter(name='Comision de Seguimiento').exists()


def es_departamento(user):
    return user.groups.filter(name='Departamento Academico').exists()


def es_tribunal(user):
    return user.groups.filter(name='Tribunal').exists()

def es_movimientos(user):
    grupos_permiso = ['Tribunal', 'Comision de Seguimiento', 'Departamento Academico']

    return user.groups.filter(name__in=grupos_permiso).exists()


def enlace_usuario_persona(user, persona, grupo):
    if grupo == 'Estudiante':
        usuario_persona = Usuario_persona(user=user, estudiante=persona, asesor=None, docente=None, tipo="estudiante")
        usuario_persona.save()
    elif grupo == 'Docente':
        usuario_persona = Usuario_persona(user=user, estudiante=None, asesor=None, docente=persona, tipo="docente")
        usuario_persona.save()
    else:
        usuario_persona = Usuario_persona(user=user, estudiante=None, asesor=persona, docente=None, tipo="asesor")
        usuario_persona.save()