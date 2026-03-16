from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name="login"),
    path('registro/',views.registro,name="registro"),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('home/',views.home,name='home'),
    path('nuevoUsuario/',views.nuevoUsuario,name='nuevoUsuario'),
    path('guardarUsuario/',views.guardarUsuario,name='guardarUsuario'),
    path('listado_usuarios/',views.listado_usuarios,name='listado_usuarios'),
    path('editarUsuario/<int:id>/',views.editarUsuario,name='editarUsuario'),
    path('procesoActualizarUsuario/',views.procesoActualizarUsuario,name='procesoActualizarUsuario'),
    path('eliminarUsuario/<int:id>/',views.eliminarUsuario,name='eliminarUsuario'),

    path('nuevaSesion/',views.nuevaSesion,name='nuevaSesion'),
    path('guardarSesion/',views.guardarSesion,name='guardarSesion'),
    path('listado_sesiones/',views.listado_sesiones,name='listado_sesiones'),
    path('editarSesion/<int:id>/',views.editarSesion,name='editarSesion'),
    path('procesoActualizarSesion/',views.procesoActualizarSesion,name='procesoActualizarSesion'),
    path('eliminarSesion/<int:id>/',views.eliminarSesion,name='eliminarSesion'),

    path('nuevaFoto/',views.nuevaFoto,name='nuevaFoto'),
    path('guardarFoto/',views.guardarFoto,name='guardarFoto'),
    path('listado_fotos/',views.listado_fotos,name='listado_fotos'),
    path('eliminarFoto/<int:id>/',views.eliminarFoto,name='eliminarFoto'),
    path('eliminarTodasLasFotos/',views.eliminarTodasLasFotos,name='eliminarTodasLasFotos'),
    path('fotos_por_sesion/<int:sesion_id>/',views.fotosPorSesion,name='fotos_por_sesion'),
    path('eliminar_fotos_sesion/<int:sesion_id>/',views.eliminarFotosSesion,name='eliminar_fotos_sesion'),

    path('nuevaSeleccion/',views.nuevaSeleccion,name='nuevaSeleccion'),
    path('guardarSeleccion/',views.guardarSeleccion,name='guardarSeleccion'),
    path('listado_selecciones/',views.listado_selecciones,name='listado_selecciones'),
    path('editarSeleccion/<int:id>/',views.editarSeleccion,name='editarSeleccion'),
    path('procesoActualizarSeleccion/',views.procesoActualizarSeleccion,name='procesoActualizarSeleccion'),
    path('eliminarSeleccion/<int:id>/',views.eliminarSeleccion,name='eliminarSeleccion'),

    path('seleccionar_fotos/',views.seleccionarFotos,name='seleccionar_fotos'),
    path('guardarSeleccionFotos/',views.guardarSeleccionFotos,name='guardarSeleccionFotos'),
    path('mis_selecciones/',views.misSelecciones,name='mis_selecciones'),
    path('ver_fotos_seleccionadas/<int:seleccion_id>/',views.verFotosSeleccionadas,name='ver_fotos_seleccionadas'),
    path('asignar_email_seleccion/<int:seleccion_id>/',views.asignarEmailSeleccion,name='asignar_email_seleccion'),
    path('enviar_seleccion/<int:seleccion_id>/',views.enviarSeleccion,name='enviarSeleccion'),
    path('cancelar_seleccion/<int:seleccion_id>/',views.cancelarSeleccion,name='cancelarSeleccion'),
    
]
