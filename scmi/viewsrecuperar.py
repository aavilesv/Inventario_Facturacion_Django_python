from random import choice
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from  django.conf import  settings
from django.core.mail import send_mail
from django.utils.html import strip_tags
def recuperar(request):
    data ={
        'titulo':'RESTAURAR CONTRASEÑA',
        'model': 'Recuperar',
        'ruta':'/scmi/recuperar/',
    }
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            try:
                with transaction.atomic():
                    if action == 'add':
                        print(request.POST['correo'])
                        longitud = 8
                        valores = "0aA1bB2cC3dD4eE5fF6gG7hH8iI9jJ9kK8lL7mM6nN5oO4pP3qQ2rR1sS0tTuUvVwWxXyYzZ"
                        datos = ""
                        datos = datos.join([choice(valores) for i in range(longitud)])
                        print(datos)
                        if User.objects.get(email=request.POST['correo'],username=request.POST['usuario']):
                            emailusuario = User.objects.get(email=request.POST['correo'],username=request.POST['usuario'])
                            asunto = 'Compra en Taller Herrera'
                            email_from = settings.EMAIL_HOST_USER
                            email_to = [emailusuario.email]
                            dato = {
                                'datos': datos,
                            }
                            user = User.objects.get(username=emailusuario.username)
                            user.set_password(datos)
                            user.save()
                            html_message = render_to_string('seguridad/cambiocontraseña.html',dato)
                            plain_message = strip_tags(html_message)
                            send_mail(asunto, plain_message, email_from, email_to, html_message=html_message,
                                      fail_silently=True)
                            messages.info(request, 'Por revisar su correo')
                            return redirect('/seguridad/logout/')
                        else:
                            messages.error(request, 'Error, Por favor ingresar datos validos')
                            return redirect('/scmi/recuperar/')

            except Exception as ex:
                messages.error(request, 'Error,''Por favor ingresar datos validos')
            return redirect('/scmi/recuperar/')
    else:
        return render(request, 'seguridad/pages-forget.html', data)
