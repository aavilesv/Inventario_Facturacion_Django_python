from django.contrib.auth.decorators import login_required
from tesisval.funciones import addUserData
from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect
from scmi.models import User
from django.contrib import messages
from django.http import HttpResponse
import json
@login_required(login_url='/seguridad/login/')
def usuario(request):
    data = {
        'titulo': 'USUARIO',
        'model': 'USUARIO',
        'ruta': '/scmi/usuario/',
        'user': request.user.username,
    }
    addUserData(request, data)
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            try:
                with transaction.atomic():
                    if action == 'contra':
                        if request.POST['nuevacontraseña'] == request.POST['confirmarcontraseña']:
                            user = User.objects.get(username=request.user.username)
                            user.set_password(request.POST['nuevacontraseña'])
                            user.save()
                    if action == 'edit':
                        user = User.objects.get(pk=request.user.id)
                        user.username=request.POST['username']
                        user.first_name = request.POST['first_name']
                        user.last_name = request.POST['last_name']
                        user.email = request.POST['email']
                        user.save()

                        pass
            except Exception as ex:
                messages.error(request, 'Usuario ya registrado:' + request.POST['username'] + ', Dato no guardado')
            return redirect('/scmi/usuario/')
    else:
        # Por primera vez viaja por Get
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            if action == 'edit':
                id = request.GET['id']
                data['id'] = id
                data['usuario'] = User.objects.get(pk=request.user.id)
                return render(request, 'seguridad/usuario_from.html', data)
            if action == 'verificar':

                try:
                    with transaction.atomic():
                        if 'contraseña' in request.GET:
                            print(request.GET['contraseña'])

                            print(request.GET['contraseña'])

                            print(request.user.password)


                            user = User.objects.get(pk=request.user.id)
                            if user.check_password(request.GET['contraseña']):

                                return HttpResponse(json.dumps({"resp": True}), content_type="application/json")
                            else:
                                return HttpResponse(json.dumps({"resp": False, "mensaje": "contraseña no valida"}),
                                                    content_type="application/json")


                    return HttpResponse(json.dumps({"resp": True}), content_type="application/json")

                except IntegrityError as ex:

                    return HttpResponse(json.dumps({"resp": False, "mensaje": str(ex)}),
                                        content_type="application/json")



        else:
            # Viaja por get cuando hay busqueda con criterio
            criterio = None
            if 'criterio' in request.GET:
                criterio = request.GET['criterio'].upper()
            if criterio:
                # Entra por criterio de busqueda
                pass
                data['criterio'] = criterio
            else:
                # La primera vez viaje por get sin criterio: consulta todos los datos
                pass
            data['usuario'] = User.objects.get(pk=request.user.id)

            return render(request, 'seguridad/usuario.html', data)

