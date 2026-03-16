from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Usuario

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