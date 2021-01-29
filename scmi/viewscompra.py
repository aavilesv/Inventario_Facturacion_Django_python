from django.db.models import Q
import datetime
import json
from django.contrib.auth.decorators import login_required
from tesisval.funciones import addUserData, MiPaginador
from django.db import transaction, IntegrityError
from django.shortcuts import render
from scmi.models import  Material, Inventario, CliProentidad, Compra, Comprainventario, Empresa,month_string_to_number
from django.http import HttpResponse
@login_required(login_url='/seguridad/login/')
def compra(request):
    data = {
        'titulo': 'CONSULTA DE COMPPRA',
        'model': 'COMPRA',
        'ruta': '/scmi/compra/',
        'user': request.user.username,
    }
    addUserData(request, data)
    if 'action' in request.GET:
        action = request.GET['action']
        data['action'] = action
        if action == 'cargarcompra':
            try:
                with transaction.atomic():
                    ventajson = json.loads(request.GET['compra'])
                    proveedor = ventajson['proveedor']
                    total = ventajson['total']
                    proveedorr= CliProentidad.objects.get(pk=int(proveedor))
                    compra = Compra()
                    compra.cliProentidad = proveedorr
                    compra.total=float(total)
                    compra.fecha= datetime.datetime.now()
                    compra.save()
                    for item in ventajson['items']:
                        artid = int(item['id']);
                        material =Material.objects.get(pk=artid)

                        detalle = Comprainventario()
                        detalle.salidacompra=compra
                        detalle.material=material
                        detalle.cantidad=int(item['cantidad'])
                        detalle.valor=float(item['precio'])
                        detalle.save()
                        material.stock += int(item['cantidad'])
                        material.save()
                        if Inventario.objects.filter(material_id=material.id).exists():
                            inventa = Inventario()
                            inventa.material=material
                            inventa.tipoinventario=1
                            inventa.cantidad = int(item['cantidad'])
                            inventa.precio=float(item['precio'])
                            inventa.save()
                    return HttpResponse(json.dumps({"resp": True}), content_type="application/json")
            except IntegrityError as ex:
                return HttpResponse(json.dumps({"resp": False, "mensaje": str(ex)}),
                                    content_type="application/json")

        if action == 'addcompra':
            data['proveedores'] = CliProentidad.objects.filter(tipo=2,status=True)
            data['material'] = Material.objects.filter(status=True)
            data['fecha'] = datetime.date.today()
            return render(request, 'scmi/compra_form.html', data)

        if action == 'ver':
            id = request.GET['id']
            data['compraa'] = Compra.objects.get(pk=id)
            data['detallee'] = Comprainventario.objects.filter(salidacompra=data['compraa'])
            data['empresa'] = Empresa.objects.get(user=request.user)
            return render(request, 'scmi/detalle_listado.html', data)
    else:
        # Viaja por get cuando hay busqueda con criterio
        criterio = None
        if 'criterio' in request.GET:
            o, p = month_string_to_number(request.GET['criterio'].capitalize())
            criterio = request.GET['criterio'].upper()
        if criterio:
            ba = True
            if criterio.isdigit():
                try:
                    ba = False

                    if Compra.objects.filter(fecventa__day=int(criterio)).exists() or Compra.objects.filter(
                            fecventa__year=int(criterio)).exists():
                        compras = Compra.objects.filter(Q(fecha__day=criterio) | Q(fecha__year=criterio)).order_by(
                            '-fecha')
                except:
                    ba = True
                    compras = Compra.objects.filter(cliProentidad__tipo=2).order_by('-fecha')
            if p:
                compras = Compra.objects.filter(fecha__month=o).order_by('-fecha')
            elif ba:
                compras = Compra.objects.filter( Q(cliProentidad__nombre__contains=criterio) | Q(cliProentidad__ced_ruc__contains=criterio)).order_by('-fecha')




            data['criterio'] = criterio
        else:
            # La primera vez viaje por get sin criterio: consulta todos los datos
            compras = Compra.objects.filter(cliProentidad__tipo=2).order_by('-fecha')
        data['compras'] = compras
        # Pagineo
        paging = MiPaginador(compras, 8)
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
        data['compras'] = page.object_list
        return render(request, 'scmi/compra_listado.html', data)
