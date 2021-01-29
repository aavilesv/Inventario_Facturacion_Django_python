import json
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from tesisval.funciones import addUserData, MiPaginador
from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect
from scmi.models import CliProentidad, Pedidoarticulo, Articulo,Pedido,month_string_to_number
from django.http import HttpResponse
@login_required(login_url='/seguridad/login/')
def pedido(request):
    data = {
        'titulo': 'LISTADO DE PEDIDO ARTICULO',
        'model': 'PEDIDO DE ARTICULO',
        'ruta': '/scmi/pedido/',
        'user': request.user.username,
    }
    addUserData(request, data)
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            try:
                with transaction.atomic():
                    if action == 'elim':
                        pedido = Pedido.objects.get(id=request.POST['id'])
                        pedido.status = False
                        pedido.save()
            except Exception as ex:
                return HttpResponse(ex)
            return redirect('/scmi/pedido/')
    else:
        # Por primera vez viaja por Get
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            if action == 'pedido':
                try:
                    with transaction.atomic():
                        ventajson = json.loads(request.GET['pedido'])
                        cliente = ventajson['cliente']
                        cliente = CliProentidad.objects.get(pk=int(cliente))
                        fecha = ventajson['fecha']+' '+ventajson['hora']+':00-05'
                        pedido = Pedido()
                        pedido.fecentrega =fecha
                        pedido.coutainicial= ventajson['subtotal']
                        pedido.cliProentidad = cliente
                        pedido.abono =ventajson['presupuesto']
                        pedido.save()
                        for item in ventajson['items']:
                            artid = int(item['id'])
                            if Articulo.objects.filter(id=artid).exists():
                                detalle = Pedidoarticulo()
                                detalle.pedido = pedido
                                detalle.articulo = Articulo.objects.get(pk=artid)
                                detalle.cantidad = int(item['cantidad'])
                                detalle.abono = float(item['abono'])
                                detalle.save()
                        return HttpResponse(json.dumps({"resp": True}), content_type="application/json")
                except IntegrityError as ex:
                    return HttpResponse(json.dumps({"resp": False, "mensaje": str(ex)}),
                                        content_type="application/json")
            if action == 'add':
                data['Articulo'] = Articulo.objects.all()
                data['cliente'] = CliProentidad.objects.filter(tipo=1)
                return render(request, 'inventario/pedido_from.html', data)
            if action == 'ver':
                id = request.GET['id']
                data['id'] = id
                data['pedido'] = Pedido.objects.get(pk=id)
                data['pedidodetalle'] = Pedidoarticulo.objects.filter(pedido=data['pedido'])
                return render(request, 'inventario/pedidodetalle.html', data)
        else:
            # Viaja por get cuando hay busqueda con criterio
            pedido = Pedido.objects.filter(status=True).order_by('-fecentrega')
            criterio = None
            if 'criterio' in request.GET:
                o, p = month_string_to_number(request.GET['criterio'].capitalize())
                criterio = request.GET['criterio'].upper()
            if criterio:
                ban = True
                if criterio.isdigit():
                    try:
                        ban = False
                        if Pedido.objects.filter(fecentrega__day=int(criterio)).exists() or Pedido.objects.filter(fecentrega__year=int(criterio)).exists():
                            pedido = Pedido.objects.filter(Q(fecentrega__day=criterio) | Q(fecentrega__year=criterio),status=True).order_by('-fecentrega')

                    except:
                        ban=True
                        pedido = Pedido.objects.filter(status=True).order_by('-fecentrega')
                if p:
                    pedido = Pedido.objects.filter(fecentrega__month=o ,status=True).order_by('-fecentrega')
                elif ban:
                    pedido = Pedido.objects.filter(Q(cliProentidad__nombre__contains=criterio) | Q(cliProentidad__ced_ruc__contains=criterio),status=True).order_by('-fecentrega')
                data['criterio'] = criterio
            else:
               # La primera vez viaje por get sin criterio: consulta todos los datos
                pedido = Pedido.objects.filter(status=True).order_by('-fecentrega')
            data['pedido'] = pedido
            # Pagineo
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
            return render(request, 'inventario/pedido_listar.html', data)

