from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.utils import timezone
import os
from .models import Usuario, SesionFotos, Foto, SeleccionCliente, FotoSeleccionada

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
            request.session["usuario_nombre"] = usuario.nombre

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

def eliminarTodasLasFotos(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    if request.session.get('rol') != 'ADMIN':
        messages.error(request, "No tienes permisos para eliminar fotos")
        return redirect('listado_fotos')
    
    Foto.objects.all().delete()
    messages.success(request, "Todas las fotos han sido eliminadas")
    return redirect('listado_fotos')

def fotosPorSesion(request, sesion_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    sesion = get_object_or_404(SesionFotos, id=sesion_id)
    fotos = Foto.objects.filter(sesion=sesion)
    
    return render(request, "Foto/fotosPorSesion.html", {
        'sesion': sesion,
        'fotos': fotos
    })

def eliminarFotosSesion(request, sesion_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    if request.session.get('rol') != 'ADMIN':
        messages.error(request, "No tienes permisos para eliminar fotos")
        return redirect('listado_fotos')
    
    if request.method == 'POST':
        fotos_a_eliminar = request.POST.getlist('fotos_seleccionadas')
        
        if fotos_a_eliminar:
            Foto.objects.filter(id__in=fotos_a_eliminar).delete()
            messages.success(request, f"Se eliminaron {len(fotos_a_eliminar)} fotos")
        else:
            messages.warning(request, "No seleccionaste ninguna foto")
    
    return redirect('fotos_por_sesion', sesion_id=sesion_id)

#--------------------
#SELECCION CLIENTE
#--------------------
def nuevaSeleccion(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    clientes = Usuario.objects.filter(rol='CLIENTE')
    return render(request, "SeleccionCliente/nuevaSeleccion.html", {
        "clientes": clientes
    })

def guardarSeleccion(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    if request.method == "POST":
        cliente_id = request.POST["cliente"]
        email_cliente = request.POST["email_cliente"]
        
        cliente = Usuario.objects.get(id=cliente_id)
        
        SeleccionCliente.objects.create(
            cliente=cliente,
            email_cliente=email_cliente
        )
        
        messages.success(request, "Selección de cliente creada correctamente")
        return redirect('listado_selecciones')
    
    messages.error(request, "Método no permitido")
    return redirect('nuevaSeleccion')

def listado_selecciones(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    selecciones = SeleccionCliente.objects.all()
    return render(request, "SeleccionCliente/listadoSeleccion.html", {
        "selecciones": selecciones
    })

def editarSeleccion(request, id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    seleccion = get_object_or_404(SeleccionCliente, id=id)
    clientes = Usuario.objects.filter(rol='CLIENTE')
    
    return render(request, "SeleccionCliente/editarSeleccion.html", {
        "seleccionEditar": seleccion,
        "clientes": clientes
    })

def procesoActualizarSeleccion(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    if request.method == "POST":
        id_seleccion = request.POST.get('id')
        seleccion = SeleccionCliente.objects.get(id=id_seleccion)
        
        cliente_id = request.POST.get('cliente')
        email_cliente = request.POST.get('email_cliente')
        
        cliente = Usuario.objects.get(id=cliente_id)
        
        seleccion.cliente = cliente
        seleccion.email_cliente = email_cliente
        seleccion.save()
        
        messages.success(request, "Selección actualizada correctamente")
        return redirect('listado_selecciones')
    
    return redirect('listado_selecciones')

def eliminarSeleccion(request, id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    seleccion = get_object_or_404(SeleccionCliente, id=id)
    seleccion.delete()
    messages.success(request, "Selección eliminada correctamente")
    return redirect('listado_selecciones')

#--------------------
#FOTO SELECCIONADA (PARA CLIENTES)
#--------------------
def seleccionarFotos(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    # Solo CLIENTES pueden seleccionar fotos
    if request.session.get('rol') != 'CLIENTE':
        messages.error(request, "Solo los clientes pueden seleccionar fotos")
        return redirect('home')
    
    fotos = Foto.objects.all()
    return render(request, "FotoSeleccionada/seleccionarFotos.html", {
        "fotos": fotos
    })

def guardarSeleccionFotos(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    # Solo CLIENTES pueden seleccionar fotos
    if request.session.get('rol') != 'CLIENTE':
        messages.error(request, "Solo los clientes pueden seleccionar fotos")
        return redirect('home')
    
    if request.method == 'POST':
        fotos_seleccionadas = request.POST.getlist('fotos_seleccionadas')
        
        if not fotos_seleccionadas:
            messages.warning(request, "No seleccionaste ninguna foto")
            return redirect('seleccionar_fotos')
        
        # Obtener el cliente actual
        cliente = Usuario.objects.get(id=request.session['usuario_id'])
        
        # Crear o actualizar la selección del cliente
        seleccion, created = SeleccionCliente.objects.get_or_create(
            cliente=cliente,
            defaults={'email_cliente': cliente.email}
        )
        
        # Eliminar selecciones anteriores de este cliente
        FotoSeleccionada.objects.filter(seleccion=seleccion).delete()
        
        # Guardar nuevas selecciones
        for foto_id in fotos_seleccionadas:
            foto = Foto.objects.get(id=foto_id)
            FotoSeleccionada.objects.create(
                seleccion=seleccion,
                foto=foto
            )
        
        messages.success(request, f"¡Perfecto! Has seleccionado {len(fotos_seleccionadas)} fotos. El administrador recibirá tu selección.")
        return redirect('mis_selecciones')
    
    return redirect('seleccionar_fotos')

def misSelecciones(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    # Solo CLIENTES pueden ver sus selecciones
    if request.session.get('rol') != 'CLIENTE':
        messages.error(request, "Esta sección es solo para clientes")
        return redirect('home')
    
    cliente = Usuario.objects.get(id=request.session['usuario_id'])
    selecciones = SeleccionCliente.objects.filter(cliente=cliente)
    
    return render(request, "FotoSeleccionada/misSelecciones.html", {
        "selecciones": selecciones
    })

def verFotosSeleccionadas(request, seleccion_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    seleccion = get_object_or_404(SeleccionCliente, id=seleccion_id)
    fotos_seleccionadas = FotoSeleccionada.objects.filter(seleccion=seleccion)
    
    return render(request, "FotoSeleccionada/verFotosSeleccionadas.html", {
        "seleccion": seleccion,
        "fotos": fotos_seleccionadas
    })

def asignarEmailSeleccion(request, seleccion_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    # Solo ADMIN puede asignar emails
    if request.session.get('rol') != 'ADMIN':
        messages.error(request, "No tienes permisos para asignar emails")
        return redirect('listado_selecciones')
    
    seleccion = get_object_or_404(SeleccionCliente, id=seleccion_id)
    
    if request.method == 'POST':
        email_destino = request.POST.get('email_destino')
        seleccion.email_cliente = email_destino
        seleccion.save()
        
        messages.success(request, f"Email asignado correctamente: {email_destino}")
        return redirect('listado_selecciones')
    
    return render(request, "FotoSeleccionada/asignarEmail.html", {
        "seleccion": seleccion
    })

def enviarSeleccion(request, seleccion_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    # Solo ADMIN puede enviar emails
    if request.session.get('rol') != 'ADMIN':
        messages.error(request, "No tienes permisos para enviar emails")
        return redirect('listado_selecciones')
    
    seleccion = get_object_or_404(SeleccionCliente, id=seleccion_id)
    fotos_seleccionadas = FotoSeleccionada.objects.filter(seleccion=seleccion)
    
    # Verificar que haya fotos seleccionadas y email asignado
    if not fotos_seleccionadas.exists():
        messages.error(request, "No hay fotos seleccionadas para enviar")
        return redirect('listado_selecciones')
    
    if not seleccion.email_cliente:
        messages.error(request, "Primero debes asignar un email de destino")
        return redirect('asignar_email_seleccion', seleccion_id=seleccion_id)
    
    try:
        # Crear email con adjuntos
        email = EmailMessage(
            subject=f'Fotos seleccionadas por {seleccion.cliente.nombre}',
            body=f'''
Hola, {seleccion.email_cliente}

Te enviamos las fotos que has seleccionado de nuestra galería.

Cliente: {seleccion.cliente.nombre}
Fecha de selección: {seleccion.fecha|date:"d/m/Y H:i"}
Total de fotos: {fotos_seleccionadas.count()}

Esperamos que disfrutes tus fotos seleccionadas.

Saludos,
Arcano Fotografía
            ''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[seleccion.email_cliente],
        )
        
        # Adjuntar las fotos
        for foto_seleccionada in fotos_seleccionadas:
            foto_path = foto_seleccionada.foto.imagen.path
            if os.path.exists(foto_path):
                email.attach_file(foto_path)
        
        # Enviar email
        email.send()
        
        # Actualizar estado y fecha de envío
        seleccion.estado = 'ENVIADO'
        seleccion.fecha_envio = timezone.now()
        seleccion.save()
        
        messages.success(request, f"¡Email enviado exitosamente a {seleccion.email_cliente} con {fotos_seleccionadas.count()} fotos!")
        
    except Exception as e:
        messages.error(request, f"Error al enviar email: {str(e)}")
    
    return redirect('listado_selecciones')

def cancelarSeleccion(request, seleccion_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    seleccion = get_object_or_404(SeleccionCliente, id=seleccion_id)
    
    # Solo puede cancelar el cliente dueño de la selección o el admin
    if request.session.get('rol') == 'CLIENTE' and seleccion.cliente.id != request.session['usuario_id']:
        messages.error(request, "No puedes cancelar esta selección")
        return redirect('mis_selecciones')
    
    if request.method == 'POST':
        notas = request.POST.get('notas_cancelacion', '')
        
        seleccion.estado = 'CANCELADO'
        seleccion.notas_cancelacion = notas
        seleccion.save()
        
        messages.success(request, "La selección ha sido cancelada")
        
        if request.session.get('rol') == 'CLIENTE':
            return redirect('mis_selecciones')
        else:
            return redirect('listado_selecciones')
    
    return render(request, "SeleccionCliente/cancelarSeleccion.html", {
        "seleccion": seleccion
    })