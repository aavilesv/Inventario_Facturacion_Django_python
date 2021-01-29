import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
from tesisval.funciones import  addUserData, MiPaginador
from django.db import  transaction
from django.shortcuts import render, redirect
from scmi.models import   Material,Inventario,Pedidodetalle
@login_required(login_url='/seguridad/login/')
def usomaterial(request):
    data ={
        'titulo':'CONSULTA DE REGISTRO DE USO DE MATERIAL',
        'model': 'REGISTRO DE USO DE MATERIAL',
        'ruta':'/scmi/detallepedido/',
        'user': request.user.username,
    }
    addUserData(request, data)
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            try:
                with transaction.atomic():
                    if action == 'add':
                        materiall =Pedidodetalle(cantidad=request.POST['cantidad'],
                                                 material=Material.objects.get(pk=request.POST['material']),
                                                 descripcion=request.POST['descripcion'].capitalize())
                        materiall.save()
                        invent =Inventario()
                        invent.material=Material.objects.get(pk=request.POST['material'])
                        invent.cantidad = request.POST['cantidad']
                        invent.fechaingreso = None
                        invent.fechasalida=datetime.datetime.now()
                        print(str(datetime.datetime.now()))
                        invent.tipoinventario = 4
                        invent.save()
                        mater=Material.objects.get(pk=request.POST['material'])
                        mater.stock-= int(request.POST['cantidad'])
                        mater.save()
                    if action == 'edit':
                        materiall = Pedidodetalle.objects.get(pk=request.POST['id'])
                        materiall.cantidad=request.POST['cantidad']
                        materiall.material=Material.objects.get(pk=request.POST['material'])
                        materiall.descripcion=request.POST['descripcion'].capitalize()
                        materiall.save()
                        invent = Inventario()
                        invent.material = Material.objects.get(pk=request.POST['material'])
                        invent.cantidad = request.POST['cantidad']
                        invent.fechaingreso = None
                        invent.fechasalida = datetime.datetime.now()
                        invent.tipoinventario = 3
                        invent.save()
                        mater = Material.objects.get(pk=request.POST['material'])
                        mater.stock -= int(request.POST['cantidad'])
                        mater.save()
            except Exception as ex:
                messages.error(request, 'Error, stock no valido')
            return redirect('/scmi/detallepedido/')
    else:
        # Por primera vez viaja por Get
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            if action == 'add':
                data['material']=Material.objects.filter(stock__gte=1,status=True)

            if action == 'edit':
                id = request.GET['id']
                data['id'] = id
                material= Pedidodetalle.objects.get(pk=id)
                data['materiall'] = Material.objects.get(pk=material.material.id,status=True)
                data['detalle'] = Pedidodetalle.objects.get(pk=id)
            return render(request, 'inventario/salidaMaterial_form.html', data)
        else:
            # Viaja por get cuando hay busqueda con criterio
            criterio = None
            if 'criterio' in request.GET:
                criterio = request.GET['criterio'].upper()
            if criterio:
                # Entra por criterio de busqueda
                pedido = Pedidodetalle.objects.filter(material__material__contains=criterio)
                data['criterio'] = criterio
            else:
                # La primera vez viaje por get sin criterio: consulta todos los datos
                pedido= Pedidodetalle.objects.filter(material__status=True)
            data['pedido']=pedido
            #Pagineo
            paging = MiPaginador(pedido, 8)
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
            data['pedido'] = page.object_list
            return render(request, 'inventario/SalidaMaterial.html', data)
