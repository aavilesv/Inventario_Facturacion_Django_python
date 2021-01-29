from random import choice
import json
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db import  IntegrityError
from tesisval.funciones import  addUserData
from django.db import transaction
from django.shortcuts import render, redirect
from scmi.models import CliProentidad, Empresa
from django.contrib.auth.models import User
@login_required(login_url='/seguridad/login/')
def perfil(request):
    data ={
        'titulo':'CONSULTA DE PERFIL',
        'model': 'PERFIL',
        'ruta':'/scmi/perfil/',
        'user': request.user.username,
    }
    addUserData(request, data)
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            try:
                with transaction.atomic():
                    if action == 'edit':

                        em =Empresa.objects.get(user=request.user.id)
                        em.nombre = request.POST['nombre']
                        em.cedula = request.POST['ruc']
                        em.direcion = request.POST['direccion']
                        em.celular = request.POST['Celular']
                        em.image = request.FILES['image']
                        em.save()


            except Exception as ex:
                messages.error(request,'Error al intentar cambiar')
            return redirect('/scmi/perfil/')
    else:
        # Por primera vez viaja por Get
        if 'action' in request.GET:

            action = request.GET['action']
            data['action'] = action

            if action == 'edit':
                # Por Modificacion o edit se captura el id a modificar
                id = request.GET['id']
                data['id'] = id
                # Se crea un objeto (registro) del id a modificar del modelo PoseedoTarjeta
                data['user']= User.objects.get(pk=request.user.id)
                data['empresa'] = Empresa.objects.get(user=data['user'])


            return render(request, 'seguridad/perfilfrom.html', data)
        else:
            # Viaja por get cuando hay busqueda con criterio
            criterio = None
            if 'criterio' in request.GET:
                criterio = request.GET['criterio'].upper()

            if criterio:
                # Entra por criterio de busqueda
                cliente = CliProentidad.objects.filter(nombre__icontains=criterio)
                data['criterio'] = criterio
            else:
                # La primera vez viaje por get sin criterio: consulta todos los datos
                user = Empresa.objects.get(user__id=request.user.id)
                print(user)
            data['user']=user
            return render(request, 'seguridad/perfil.html', data)
