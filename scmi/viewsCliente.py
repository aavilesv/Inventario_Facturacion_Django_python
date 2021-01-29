from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tesisval.funciones import addUserData, MiPaginador
from django.db import transaction
from django.shortcuts import render, redirect
from scmi.models import CliProentidad
@login_required(login_url='/seguridad/login/')
def cliente(request):
    data ={
        'titulo':'CONSULTA DE CLIENTE',
        'model': 'CLIENTE',
        'ruta':'/scmi/cliente/',
        'user': request.user.username,
    }
    addUserData(request, data)
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            try:
                with transaction.atomic():
                    if action == 'add':
                        cliente = CliProentidad(nombre = request.POST['nombre'].upper(),tipo = 1,direccion = request.POST['direccion'].capitalize(),telefono = request.POST['telefono'],ced_ruc =request.POST['ced_ruc'],email = request.POST['email'])
                        cliente.save()
                    if action == 'edit':
                        cliente = CliProentidad.objects.select_related().get(pk=request.POST['id'])
                        cliente.nombre = request.POST['nombre'].upper()
                        cliente.tipo = 1
                        cliente.direccion = request.POST['direccion'].capitalize()
                        cliente.telefono = request.POST['telefono']
                        cliente.ced_ruc = request.POST['ced_ruc']
                        cliente.email = request.POST['email']
                        cliente.save()
                    if action == 'elim':
                        id = request.POST['id']
                        data['id'] = id
                        cliente = CliProentidad.objects.get(pk=id)
                        cliente.status=False
                        cliente.save()
            except Exception as ex:
                messages.error(request,'Cédula ya registrada:'+request.POST['ced_ruc']+', Dato no guardado')
            return redirect('/scmi/cliente/')
    else:
        # Por primera vez viaja por Get
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            if action == 'edit':
                id = request.GET['id']
                data['id'] = id
                data['proveedor']= CliProentidad.objects.get(pk=id)
            return render(request, 'facturacion/cliente_from.html', data)
        else:
            # Viaja por get cuando hay busqueda con criterio
            criterio = None
            if 'criterio' in request.GET:
                criterio = request.GET['criterio'].upper()
            if criterio:
                # Entra por criterio de busqueda
                if criterio.isdigit():
                    cliente = CliProentidad.objects.filter(ced_ruc__icontains=criterio)
                else:
                    cliente = CliProentidad.objects.filter(nombre__icontains=criterio)
                data['criterio'] = criterio
            else:
                # La primera vez viaje por get sin criterio: consulta todos los datos
                cliente = CliProentidad.objects.filter(tipo=1)
            data['cliente']=cliente
            #Pagineo
            paging = MiPaginador(cliente, 8)
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
            data['cliente'] = page.object_list
            return render(request, 'facturacion/cliente.html', data)
