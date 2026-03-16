#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Foto.settings')
django.setup()

from Aplicaciones.lente.models import Usuario

print("=== USUARIOS EXISTENTES ===")
print()

if Usuario.objects.exists():
    for usuario in Usuario.objects.all():
        print(f" {usuario.nombre}")
        print(f"    Email: {usuario.email}")
        print(f"    Rol: {usuario.rol}")
        print(f"    Fecha: {usuario.fecha_registro}")
        print("-" * 40)
else:
    print(" No hay usuarios registrados")

print()
print(f"Total de usuarios: {Usuario.objects.count()}")
print()
print("Roles disponibles:")
print("- ADMIN: Administrador del sistema")
print("- CLIENTE: Cliente que puede seleccionar fotos")
