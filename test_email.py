#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Foto.settings')
django.setup()

from django.core.mail import EmailMessage
from django.conf import settings

def test_email_config():
    """Probar la configuración de email"""
    print("=== CONFIGURACIÓN EMAIL ===")
    print(f"Backend: {settings.EMAIL_BACKEND}")
    print(f"Host: {settings.EMAIL_HOST}")
    print(f"Port: {settings.EMAIL_PORT}")
    print(f"Use TLS: {settings.EMAIL_USE_TLS}")
    print(f"Use SSL: {settings.EMAIL_USE_SSL}")
    print(f"From: {settings.DEFAULT_FROM_EMAIL}")
    print()

def test_send_email():
    """Enviar email de prueba"""
    try:
        email = EmailMessage(
            subject='[Arcano Fotografía] Prueba de Envío',
            body='''
Hola,

Este es un email de prueba para verificar que la configuración funciona correctamente.

Si recibes este email, significa que el sistema está listo para enviar fotos a clientes.

Saludos,
Arcano Fotografía
            '''.strip(),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=['abraham.nacimba5565@utc.edu.ec'],  # Cambia esto para probar
        )
        
        email.send()
        print("✅ Email enviado exitosamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error al enviar email: {e}")
        return False

if __name__ == '__main__':
    print("🧪 Probando configuración de email...\n")
    
    test_email_config()
    
    print("📧 Enviando email de prueba...")
    success = test_send_email()
    
    if success:
        print("\n🎉 El sistema de email está funcionando correctamente!")
        print("Ya puedes enviar fotos a los clientes.")
    else:
        print("\n⚠️ Hay problemas con la configuración de email.")
        print("Verifica:")
        print("1. Que la contraseña de aplicación sea correcta")
        print("2. Que tengas acceso al correo")
        print("3. Que no haya firewall bloqueando el puerto 587")
