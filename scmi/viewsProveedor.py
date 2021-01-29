from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tesisval.funciones import addUserData, MiPaginador
from django.db import transaction
from django.shortcuts import render, redirect
from scmi.models import CliProentidad
@login_required(login_url='/seguridad/login/')
def proveedor(request):
    data ={
        'titulo':'CONSULTA DE PROVEEDOR',
        'model': 'PROVEEDOR',
        'ruta':'/scmi/proveedor/',
        'user': request.user.username,
    }
    addUserData(request, data)
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            try:
                with transaction.atomic():
                    if action == 'add':
                        proveedor = CliProentidad(nombre=request.POST['nombre'].upper(), tipo=2,
                                                  direccion=request.POST['direccion'].capitalize(),
                                                  telefono=request.POST['telefono'], ced_ruc=request.POST['ced_ruc'],email = request.POST['email'])

                        proveedor.save()
                    if action == 'edit':
                        proveedor = CliProentidad.objects.select_related().get(pk=request.POST['id'])
                        proveedor.nombre = request.POST['nombre'].upper()
                        proveedor.tipo = 2
                        proveedor.direccion = request.POST['direccion'].capitalize()
                        proveedor.telefono = request.POST['telefono']
                        proveedor.ced_ruc = request.POST['ced_ruc']
                        proveedor.email = request.POST['email']
                        proveedor.save()
                    if action == 'elim':
                        id = request.POST['id']
                        data['id'] = id
                        proveedor = CliProentidad.objects.get(pk=id)
                        proveedor.status=False
                        proveedor.save()
            except Exception as ex:
                messages.error(request, 'Cédula ya registrada:' + request.POST['ced_ruc'] + ', Dato no guardado')
            return redirect('/scmi/proveedor/')
    else:
        # Por primera vez viaja por Get
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            if action == 'edit':
                # Por Modificacion o edit se captura el id a modificar
                id = request.GET['id']
                data['id'] = id
                data['proveedor'] = CliProentidad.objects.get(pk=id)
            proveedora = CliProentidad.objects.filter(tipo=2)
            data['proveedora'] = proveedora
            return render(request, 'scmi/proveedor_form.html', data)
        else:
            # Viaja por get cuando hay busqueda con criterio
            criterio = None
            if 'criterio' in request.GET:
                criterio = request.GET['criterio'].upper()
            if criterio:
                # Entra por criterio de busqueda
                if criterio.isdigit():
                    proveedor = CliProentidad.objects.filter(tipo=2, ced_ruc__icontains=criterio, status=True)
                else:
                    proveedor = CliProentidad.objects.filter(tipo=2,nombre__icontains=criterio,status=True)
                data['criterio'] = criterio
            else:
                # La primera vez viaje por get sin criterio: consulta todos los datos
                proveedor = CliProentidad.objects.filter(tipo=2,status=True)
            data['proveedor']=proveedor
            #Pagineo
            paging = MiPaginador(proveedor, 8)
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
            data['proveedor'] = page.object_list
            return render(request, 'scmi/proveedor_listar.html', data)
