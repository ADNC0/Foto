from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('nuevoUsuario/',views.nuevoUsuario,name='nuevoUsuario'),
    path('guardarUsuario/',views.guardarUsuario,name='guardarUsuario'),
    path('listado_usuarios/',views.listado_usuarios,name='listado_usuarios'),
    path('editarUsuario/<int:id>/',views.editarUsuario,name='editarUsuario'),
    path('procesoActualizarUsuario/',views.procesoActualizarUsuario,name='procesoActualizarUsuario'),
    path('eliminarUsuario/<int:id>/',views.eliminarUsuario,name='eliminarUsuario'),
]
