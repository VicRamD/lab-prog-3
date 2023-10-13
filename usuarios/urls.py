from django.urls import path

from gestion import views as g_v
from usuarios import views

app_name = 'usuarios'
urlpatterns = [
    path('', g_v.index, name='index'),
    path('index/', views.index_logeado, name='index_login'),
    path('login/', views.login_view, name='login'),
    #path('logout', views.logout_view, name='logout')
]