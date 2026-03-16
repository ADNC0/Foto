from django.contrib import admin
from .models import Usuario, SesionFotos, Foto, SeleccionCliente, FotoSeleccionada

# Register your models here.
admin.site.register(Usuario)
admin.site.register(SesionFotos)
admin.site.register(Foto)
admin.site.register(SeleccionCliente)
admin.site.register(FotoSeleccionada)
