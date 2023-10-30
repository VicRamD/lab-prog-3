from django.urls import path

from gestion import views as g_v
from usuarios import views

app_name = 'usuarios'
urlpatterns = [
    path('', views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("usuario/registrar/<int:id>/<str:grupo>/", views.registrar_usuario, name="registrar_usuario"),
]