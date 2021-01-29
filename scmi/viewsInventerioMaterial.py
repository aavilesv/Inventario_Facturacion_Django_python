from datetime import datetime
from django.contrib.auth.decorators import login_required
from tesisval.funciones import addUserData, MiPaginador
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from scmi.models import TipoMaterial,Material,Inventario
@login_required(login_url='/seguridad/login/')
def material(request):
    data ={
        'titulo':'CONSULTA DE INVENTARIO MATERIAL',
        'model': 'INVENTARIO  DE MATERIAL',
        'ruta':'/scmi/material/',
        'user': request.user.username,
    }
    addUserData(request, data)
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            try:
                with transaction.atomic():
                    if action == 'add':
                        materiall =Material(material=request.POST['material'].upper(),tipo=TipoMaterial.objects.get(pk=request.POST['tipo']),arprecio=request.POST['arprecio']
                                            ,stock=request.POST['stock'])

                        materiall.save()
                        invent =Inventario()
                        invent.material=materiall
                        invent.cantidad = request.POST['stock']
                        invent.precio=request.POST['arprecio']
                        invent.fechaingreso = datetime.now()
                        invent.tipoinventario = 2
                        invent.save()
                    if action == 'edit':
                        materiall = Material.objects.select_related().get(pk=request.POST['id'])
                        materiall.material=request.POST['material'].upper()
                        materiall.tipo=TipoMaterial.objects.get(pk=request.POST['tipo'])
                        materiall.arprecio=request.POST['arprecio']
                        materiall.stock=request.POST['stock']
                        materiall.save()
                        invent = Inventario()
                        invent.material = materiall
                        invent.cantidad = request.POST['stock']
                        invent.precio = request.POST['arprecio']
                        invent.fechaingreso = datetime.now()
                        invent.tipoinventario = 3
                        invent.save()
                    if action == 'elim':
                        materiall = Material.objects.get(pk=request.POST['id'])
                        materiall.status = False
                        materiall.save()
            except Exception as ex:
                return HttpResponse(ex)
            return redirect('/scmi/material/')
    else:
        # Por primera vez viaja por Get
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            if action == 'inventario':
                id = request.GET['id']
                data['inventari'] = Inventario.objects.filter(material__id=id)
                data['id'] = id
                return render(request, 'inventario/inventario_listar.html', data)
            if action == 'add':
                data['tipo']=TipoMaterial.objects.all()
            if action == 'edit':
                id = request.GET['id']
                data['id'] = id
                material=Material.objects.get(pk=id)
                data['material']= material
                data['tipo'] = TipoMaterial.objects.all()
                data['tipoo'] = TipoMaterial.objects.get(pk=material.tipo.id)
            return render(request, 'mantenimiento/material_form.html', data)
        else:
            # Viaja por get cuando hay busqueda con criterio
            criterio = None
            if 'criterio' in request.GET:
                criterio = request.GET['criterio'].upper()

            if criterio:
                # Entra por criterio de busqueda
                material = Material.objects.filter(material__contains=criterio)
                data['criterio'] = criterio
            else:
                # La primera vez viaje por get sin criterio: consulta todos los datos
                material= Material.objects.filter(status=True)
            data['material']=material

            #Pagineo
            paging = MiPaginador(material, 8)
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
            data['material'] = page.object_list
            return render(request, 'mantenimiento/material.html', data)
