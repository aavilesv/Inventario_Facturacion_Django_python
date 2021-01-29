from datetime import datetime    #para importar la fecha
from django.db.models import Q
import json
from django.contrib.auth.decorators import login_required
from tesisval.funciones import addUserData, MiPaginador
from django.db import IntegrityError
from django.db import transaction
from django.shortcuts import render, redirect
from scmi.models import  Articulo, Proforma, DetalleProforma, Empresa,month_string_to_number
from django.http import HttpResponse
@login_required(login_url='/seguridad/login/')
def proforma(request):
    data = {
        'titulo': 'LISTADO DE PROFORMA',
        'model': 'PROFORMA',
        'ruta': '/scmi/proforma/',
        'user': request.user.username,
    }
    addUserData(request, data)
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            try:
                with transaction.atomic():
                    if action == 'elim':
                        id = request.POST['id']
                        data['id'] = id
                        proveedor = Proforma.objects.get(pk=id)
                        proveedor.status=False
                        proveedor.save()
            except Exception as ex:
                return HttpResponse(ex)
            return redirect('/scmi/proforma/')
    else:
        # Por primera vez viaja por Get
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            if action == 'cargar':
                try:
                    with transaction.atomic():
                        ventajson = json.loads(request.GET['compra'])
                        total = ventajson['total']
                        empresa = Empresa.objects.get(pk=int(request.user.id))
                        proforma = Proforma(empresa=empresa,total=total,status=True,descripcion=ventajson['descripcion'].upper())
                        proforma.save()
                        for item in ventajson['items']:
                            artid = int(item['id']);
                            detalle =DetalleProforma(proforma=proforma,articulo=Articulo.objects.get(pk=artid),descripcion=item['caracteristicas'],
                                                     cantidad=int(item['cantidad']),total=float(item['precio']),maximo=(float(item['precio'])*int(item['cantidad'])))
                            detalle.save()
                        return HttpResponse(json.dumps({"resp": True}), content_type="application/json")
                except IntegrityError as ex:
                    return HttpResponse(json.dumps({"resp": False, "mensaje": str(ex)}),
                                        content_type="application/json")
            if action == 'add':
                pass
            if action == 'edit':
                # Por Modificacion o edit se captura el id a modificar
                id = request.GET['id']
                proform=Proforma.objects.get(pk=int(id))
                # Se crea un objeto (registro) del id a modificar del modelo PoseedoTarjeta
                detalleproforma = DetalleProforma.objects.filter(proforma__id=proform.id)
                data['detalleproforma']=detalleproforma
                data['proform'] = proform
                return render(request, 'inventario/detalleproforma.html', data)
            data['articulo'] = Articulo.objects.filter(status=True)
            data['fecha'] = datetime.now().date()
            return render(request, 'inventario/proforma_form.html', data)
        else:
            # Viaja por get cuando hay busqueda con criterio
            criterio = None
            if 'criterio' in request.GET:
                o, p = month_string_to_number(request.GET['criterio'].capitalize())
                criterio = request.GET['criterio']
                ba = True
                if criterio.isdigit():
                    try:
                        ba = False

                        if Proforma.objects.filter(fec__day=int(criterio)).exists() or Proforma.objects.filter(
                                fec__year=int(criterio)).exists():
                            proforma = Proforma.objects.filter(Q(fec__day=criterio) | Q(fec__year=criterio),
                                                               status=True).order_by('-fec')
                    except:
                        ba = True
                        proforma = Proforma.objects.filter(status=True).order_by('-fec')
                if p:
                    proforma = Proforma.objects.filter(fec__month=o, status=True).order_by('-fec')
                elif ba:
                    proforma = Proforma.objects.filter(descripcion__contains=criterio,status=True).order_by('-fec')

                # Entra por criterio de busqueda
                data['criterio'] = criterio
            else:
               # La primera vez viaje por get sin criterio: consulta todos los datos
               proforma = Proforma.objects.filter(status=True).order_by('-fec')
            data['proforma'] = proforma
            # Pagineo
            paging = MiPaginador(proforma, 8)
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
            data['proforma'] = page.object_list
            return render(request, 'inventario/proforma.html', data)

