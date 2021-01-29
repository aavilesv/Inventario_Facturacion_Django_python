
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tesisval.funciones import  addUserData, MiPaginador
from django.db import  transaction

from django.shortcuts import render, redirect

from scmi.models import   TipoMaterial

@login_required(login_url='/seguridad/login/')

def tipomaterial(request):
    data ={
        'titulo':'CONSULTA DE TIPO DE MATERIAL',
        'model': 'TIPO DE MATERIAL',
        'ruta':'/scmi/tipomaterial/',
        'user': request.user.username,
    }
    addUserData(request, data)
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            try:
                with transaction.atomic():

                    if action == 'dato':
                       tipo  =TipoMaterial(nombre=request.POST['nombre'])
                       tipo.save()
                    if action == 'edit':

                        tipo = TipoMaterial.objects.get(pk=request.POST['id'])
                        tipo.nombre = request.POST['nombre']
                        tipo.save()

            except Exception as ex:
                messages.error(request, 'Error')


            return redirect('/scmi/tipomaterial/')
    else:
        # Por primera vez viaja por Get
        if 'action' in request.GET:

            action = request.GET['action']
            data['action'] = action


        else:
            # Viaja por get cuando hay busqueda con criterio
            criterio = None
            if 'criterio' in request.GET:
                criterio = request.GET['criterio']

            if criterio:
                # Entra por criterio de busqueda
                tipomaterial = TipoMaterial.objects.filter(nombre__contains=criterio)
                data['criterio'] = criterio
            else:
                # La primera vez viaje por get sin criterio: consulta todos los datos
                tipomaterial= TipoMaterial.objects.all()
                data['tipomaterial']=tipomaterial


            #Pagineo
            paging = MiPaginador(tipomaterial, 8)
            p = 1
            try:
                if 'page' in request.GET:
                    p = int(request.GET['page'])
                page = paging.page(p)
            except:
                page = paging.page(p)
            data['paging'] = paging
            data['rangospaging'] = paging.rangos_paginado(p)
            data['page'] = page
            data['tipomaterial'] = page.object_list

            return render(request, 'inventario/tipomaterial.html', data)
