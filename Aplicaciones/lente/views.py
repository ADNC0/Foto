from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Usuario, SesionFotos, Foto

def home(request):
    return render(request,"home.html")

def login(request):

    if request.method == "POST":

        email = request.POST["email"]
        password = request.POST["password"]

        try:

            usuario = Usuario.objects.get(email=email, password=password)

            request.session["usuario_id"] = usuario.id
            request.session["rol"] = usuario.rol

            return redirect("home")

        except Usuario.DoesNotExist:

            return render(request,"login.html",{
                "error":"Usuario o contraseña incorrectos"
            })

    return render(request,"login.html")

def registro(request):

    if request.method == "POST":
        nombre = request.POST["nombre"]
        email = request.POST["email"]
        password = request.POST["password"]

        Usuario.objects.create(
            nombre=nombre,
            email=email,
            password=password,
            rol="CLIENTE"
        )

        return redirect("login")
    return render(request,"registro.html")

def cerrar_sesion(request):
    request.session.flush()
    return redirect("login")
#---------------------
#USUARIO
#Logica de programacion sin esto las urls no funcionan, los botones no funcionan
#---------------------
def nuevoUsuario(request):
    return render(request, "Usuario/nuevousuario.html")

def guardarUsuario(request):
    if request.method == "POST":
        nombre = request.POST["nombre"]
        email = request.POST["email"]
        password = request.POST["password"]
        rol = request.POST["rol"]

        Usuario.objects.create(
            nombre=nombre,
            email=email,
            password=password,
            rol=rol
        )
        messages.success(request, "Nuevo usuario agregado con éxito.")
        return redirect('listado_usuarios')
    messages.error(request, "Método no permitido.")
    return redirect('nuevoUsuario')

def listado_usuarios(request):

    if 'usuario_id' not in request.session:
        return redirect('login')
    usuarios = Usuario.objects.all()
    return render(request,"Usuario/listadousuario.html",{
        'usuarios':usuarios
    })

def editarUsuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    return render(request, "Usuario/editarusuario.html", {
        'usuarioEditar': usuario
    })

def procesoActualizarUsuario(request):
    if request.method == "POST":
        id_usuario = request.POST.get('id')
        usuario = Usuario.objects.get(id=id_usuario)
        usuario.nombre = request.POST.get('nombre')
        usuario.email = request.POST.get('email')
        usuario.password = request.POST.get('password')
        usuario.rol = request.POST.get('rol')
        usuario.save()
        messages.success(request, "Usuario actualizado correctamente.")
        return redirect('listado_usuarios')

    return redirect('listado_usuarios')

def eliminarUsuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    usuario.delete()
    messages.success(request, "Usuario eliminado correctamente.")
    return redirect('listado_usuarios')

#---------------------
#SESION FOTOS
#Logica de programacion sin esto las urls no funcionan, los botones no funcionan
#---------------------
def nuevaSesion(request):
    administradores = Usuario.objects.filter(rol="ADMIN")
    return render(request, "SesionFotos/nuevaSesionFotos.html", {
        "administradores": administradores
    })


def guardarSesion(request):
    if request.method == "POST":
        nombre = request.POST["nombre"]
        administrador_id = request.POST["administrador"]
        administrador = Usuario.objects.get(id=administrador_id)

        SesionFotos.objects.create(
            nombre=nombre,
            administrador=administrador
        )

        messages.success(request, "Nueva sesión creada con éxito.")
        return redirect('listado_sesiones')
    messages.error(request, "Método no permitido.")
    return redirect('nuevaSesion')


def listado_sesiones(request):

    if 'usuario_id' not in request.session:
        return redirect('login')
    sesiones = SesionFotos.objects.all()
    return render(request, "SesionFotos/listadoSesionFotos.html", {
        'sesiones': sesiones
    })

def editarSesion(request, id):

    sesion = get_object_or_404(SesionFotos, id=id)
    administradores = Usuario.objects.filter(rol="ADMIN")

    return render(request, "SesionFotos/editarSesionFotos.html", {
        'sesionEditar': sesion,
        'administradores': administradores
    })


def procesoActualizarSesion(request):

    if request.method == "POST":
        id_sesion = request.POST.get('id')
        sesion = SesionFotos.objects.get(id=id_sesion)
        nombre = request.POST.get('nombre')
        administrador_id = request.POST.get('administrador')
        administrador = Usuario.objects.get(id=administrador_id)
        sesion.nombre = nombre
        sesion.administrador = administrador
        sesion.save()
        messages.success(request, "Sesión actualizada correctamente.")
        return redirect('listado_sesiones')

    return redirect('listado_sesiones')

def eliminarSesion(request, id):

    sesion = get_object_or_404(SesionFotos, id=id)
    sesion.delete()
    messages.success(request, "Sesión eliminada correctamente.")
    return redirect('listado_sesiones')

#--------------------
#FOTO
#--------------------
def nuevaFoto(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    if request.session.get('rol') != 'ADMIN':
        messages.error(request, "No tienes permisos para subir fotos")
        return redirect('listado_fotos')
    
    sesiones = SesionFotos.objects.all()
    return render(request,"Foto/nuevaFoto.html",{
        "sesiones":sesiones
    })


def guardarFoto(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    if request.session.get('rol') != 'ADMIN':
        messages.error(request, "No tienes permisos para subir fotos")
        return redirect('listado_fotos')

    if request.method == "POST":
        sesion_id = request.POST["sesion"]
        sesion = SesionFotos.objects.get(id=sesion_id)
        imagenes = request.FILES.getlist("imagenes")
        for img in imagenes:

            Foto.objects.create(
                nombre = img.name,
                imagen = img,
                sesion = sesion
            )

        messages.success(request,"Fotos cargadas correctamente")
        return redirect("listado_fotos")
    return redirect("nuevaFoto")

def listado_fotos(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    fotos = Foto.objects.all()
    return render(request,"Foto/listadoFoto.html",{
        "fotos":fotos
    })

def eliminarFoto(request, id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    if request.session.get('rol') != 'ADMIN':
        messages.error(request, "No tienes permisos para eliminar fotos")
        return redirect('listado_fotos')
    
    foto = get_object_or_404(Foto, id=id)
    foto.delete()
    messages.success(request, "Foto eliminada correctamente")
    return redirect('listado_fotos')