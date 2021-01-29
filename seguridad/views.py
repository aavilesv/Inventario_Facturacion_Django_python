

from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from scmi.models import Pedido

from tesisval.funciones import addUserData

@login_required(login_url='/seguridad/login/')
def index(request):
    data = {
        'titulo': 'TALLER HERRERA',
        'saludo': 'BIENVENIDOS',

    }
    addUserData(request,data)
    data['pedidooo'] = Pedido.objects.all()
    return render(request, 'inventario/pedidocalendario.html', data)



def login_session(request):

    data = {'titulo': 'INICIO DE SESIÓN'}

    if request.method == 'POST':
        print(request.POST)
        user = authenticate(username=request.POST['usuario'],
                            password=request.POST['password'])

        data['resp'] = False
        if user is not None:
            if user.is_active:
                login(request, user)
                data['resp'] = True
                data['user'] = user.username

            else:
                data['error'] = 'Usuario no esta Activo'
        else:
            data['error'] = 'El Usuario es Incorrecto'

        return JsonResponse(data)

    else:

        data['sistema'] = 'TALLER HERRERA'
        data['logo'] = "fas fa-spinner fa-spin"
        data['institucion'] = 'CAROLINA HERRERA'
        return render(request, 'seguridad/login.html', data)


def logout_user(request):
    logout(request)
    return redirect('/seguridad/login/')