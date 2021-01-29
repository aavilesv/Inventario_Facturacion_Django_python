from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from tesisval.funciones import addUserData
from django.db import transaction
from django.shortcuts import render, redirect
from scmi.models import Reporteventa
@login_required(login_url='/seguridad/login/')
def estadistica(request):
    data ={
        'titulo':'REPORTES',
        'model': 'ESTADISTICA',
        'ruta':'/scmi/estadistica/',
        'user': request.user.username,
    }
    addUserData(request, data)
    años=[]
    totalaños =[]
    año=0
    añoss =None
    mesaño =[]
    mesactual=[]
    totalactual =[]
    cont =0
    for c in Reporteventa.objects.all().order_by('-año'):
            if not(c.año in años) and (cont <=8) :
                años.append(c.año)
                cont+=1
                s =Reporteventa.objects.filter(año=c.año).annotate(Sum('total')).aggregate(Sum('total'))
                totalaños.append(s['total__sum'])
    data['años']=(años)
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            try:
                with transaction.atomic():
                    if action == 'estadistica':
                        año=int(request.POST['año'])
                        añoss =int(request.POST['año'])
            except Exception as ex:
                return redirect('/scmi/estadistica/')
    else:
        año = timezone.now().year
    mesañosss =[]
    porte =Reporteventa.objects.filter(año=año).order_by('mes')
    for i in porte:
        if not(current_date_format(i.mes) in mesactual):
            mesactual.append(current_date_format(i.mes))
            s = porte.filter(mes=i.mes).annotate(Sum('total')).aggregate(Sum('total'))
            totalactual.append(s['total__sum'])

    data['dat']=mesactual
    data['comprass']=totalactual
    data['totalaños']=totalaños
    data['año']=año
    data['añoss']=añoss
    data['mesaño']=mesaño
    return render(request, 'estadistica/estadisticass.html', data)
def current_date_format(month):
    months = ("Enero", "Febrero","Marzo", "Abril", "Mayo","Junio","Julio", "Agosto","Septiembre","Octubre", "Noviembre", "Diciembre")
    month = months[month - 1]
    return month

