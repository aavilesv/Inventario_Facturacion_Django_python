from django.db.models import Q
from django.utils import timezone
from django.utils.html import strip_tags
import datetime
import json
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.decorators import login_required
from tesisval.funciones import addUserData, MiPaginador
from django.db import transaction, IntegrityError
from django.shortcuts import render
from scmi.models import CliProentidad,Articulo,Detfactura,Factura,Empresa, month_string_to_number,Reporteventa
from django.http import HttpResponse
@login_required(login_url='/seguridad/login/')
def factura(request):
    data = {
        'titulo': 'CONSULTA DE FACTURA',
        'model': 'FACTURA',
        'ruta': '/scmi/factura/',
        'user': request.user.username,
    }
    addUserData(request, data)
    if 'action' in request.GET:
        action = request.GET['action']
        data['action'] = action
        if action=='cargaventa':
            try:
                with transaction.atomic():
                    vali = 0
                    cant = 0
                    ventajson = json.loads(request.GET['venta'])
                    cliente = ventajson['cliente']
                    subtotal = ventajson['subtotal']
                    total = ventajson['total']
                    cliente= CliProentidad.objects.get(pk=int(cliente))
                    iva=float(subtotal)*0.12
                    facturar = Factura()
                    facturar.cliente = cliente
                    facturar.iva=iva
                    facturar.subtotal=float(subtotal)
                    facturar.total=float(total)
                    facturar.fecventa =timezone.now()
                    facturar.save()
                    if Reporteventa.objects.filter(mes=timezone.now().month,año=timezone.now().year).exists():
                        print(datetime.datetime.now().month)
                        print(datetime.datetime.now().year)
                        reporte = Reporteventa.objects.get(mes=datetime.datetime.now().month,año=datetime.datetime.now().year)
                        reporte.total += round((float(total)))
                        reporte.save()
                    else:
                        reporte = Reporteventa()
                        reporte.mes = timezone.now().month
                        reporte.año =timezone.now().year
                        reporte.total=round((float(total)))
                        reporte.save()
                    for item in ventajson['items']:
                        artid = int(item['id']);
                        vali = int(item['id']);
                        if Articulo.objects.filter(id=artid).exists():
                            detalle = Detfactura()
                            detalle.factura=facturar
                            arct =Articulo.objects.get(pk=artid)
                            arct.cantidad -= int(item['cantidad'])
                            cant = int(item['cantidad'])
                            arct.save()
                            detalle.articulo=Articulo.objects.get(pk=artid)
                            detalle.cantidad=int(item['cantidad'])
                            detalle.total=float(item['precio'])
                            detalle.save()
                    asunto ='Compra en Taller Herrera'
                    email_from=settings.EMAIL_HOST_USER
                    data['detalle'] = Detfactura.objects.filter(factura=facturar)
                    data['empresa'] = Empresa.objects.get(user=request.user)
                    email_to=[cliente.email]
                    datos = {
                        'factura': facturar,
                        'detalle': Detfactura.objects.filter(factura=facturar),
                        'sucursal': Empresa.objects.get(user=request.user),
                    }
                    html_message = render_to_string('facturacion/correoenvio.html', datos)
                    plain_message = strip_tags(html_message)
                    send_mail(asunto,plain_message,email_from,email_to, html_message=html_message,fail_silently=True)
                    return HttpResponse(json.dumps({"resp": True}), content_type="application/json")
            except IntegrityError as ex:
                sali=""
                if Articulo.objects.filter(id=vali).exists():
                    articu= Articulo.objects.get(pk=vali)
                    sali ="Articulo ingresado:"+articu.nombre+"\nCantidad:"+str(cant)+" superada al límite de stock:"+str(articu.cantidad)

                return HttpResponse(json.dumps({"resp": False, "mensaje": sali}),
                                    content_type="application/json")
        if action == 'addfactura':
            data['clientes'] = CliProentidad.objects.filter(tipo=1,status=True)
            data['articulos'] = Articulo.objects.filter(status=True,cantidad__gte=1)
            data['fecha'] = datetime.date.today()
            return render(request, 'facturacion/factura_form.html', data)
        if action == 'ver':
            id = request.GET['id']
            data['facturaa'] = Factura.objects.get(pk=id)
            data['detalle']=Detfactura.objects.filter(factura=data['facturaa'])
            data['empresa']=Empresa.objects.get(user=request.user)
            return render(request, 'facturacion/detallefactura.html', data)
    else:
        # Viaja por get cuando hay busqueda con criterio
        factura = Factura.objects.all().order_by('-fecventa')
        criterio = None
        if 'criterio' in request.GET:
            o, p = month_string_to_number(request.GET['criterio'].capitalize())
            criterio = request.GET['criterio'].upper()
        if criterio:
            ba=True
            if criterio.isdigit():
                try:
                    ba = False
                    if Factura.objects.filter(fecventa__day=int(criterio)).exists() or Factura.objects.filter(fecventa__year=int(criterio)).exists():
                        factura = Factura.objects.filter(Q(fecventa__day=criterio) | Q(fecventa__year=criterio)).order_by('-fecventa')
                except:
                    ba=True
                    factura = Factura.objects.all().order_by('-fecventa')
            if p:
                factura = Factura.objects.filter(fecventa__month=o).order_by('-fecventa')
            elif ba:
                factura = Factura.objects.filter(Q(cliente__nombre__contains=criterio) | Q(cliente__ced_ruc__contains=criterio),cliente__tipo=1).order_by('-fecventa')
            data['criterio'] = criterio
        else:
           # La primera vez viaje por get sin criterio: consulta todos los datos
            factura = Factura.objects.all().order_by('-fecventa')
        data['venta'] = factura
        # Pagineo
        paging = MiPaginador(factura, 10)
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
        data['venta'] = page.object_list
        return render(request, 'facturacion/factura.html', data)

