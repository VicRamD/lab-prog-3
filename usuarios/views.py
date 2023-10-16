from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

def login_view(request):
    if request.method == "POST":
        usuario = request.POST["usuario"]
        password = request.POST["password"]
        user = authenticate(request, username=usuario, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("usuarios:index_login"))
        else:
            return render(request, "index.html", {"mensaje": "Los datos son incorrectos"})
    return render(request, 'login.html')

def index_logeado(request):
    return render(request, 'index.html', {"login_correcto": True})