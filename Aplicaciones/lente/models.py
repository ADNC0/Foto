from django.db import models


class Usuario(models.Model):

    ROL_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('CLIENTE', 'Cliente'),
    ]

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    rol = models.CharField(max_length=10, choices=ROL_CHOICES)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.rol}"


class SesionFotos(models.Model):

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    administrador = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Foto(models.Model):

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    imagen = models.FileField(upload_to='galeria')
    sesion = models.ForeignKey(SesionFotos, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class SeleccionCliente(models.Model):

    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    email_cliente = models.EmailField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Seleccion de {self.cliente.nombre}"


class FotoSeleccionada(models.Model):

    id = models.AutoField(primary_key=True)
    seleccion = models.ForeignKey(SeleccionCliente, on_delete=models.CASCADE)
    foto = models.ForeignKey(Foto, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.seleccion.cliente.nombre} - {self.foto.nombre}"