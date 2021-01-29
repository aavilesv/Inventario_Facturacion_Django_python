from django.urls import path
from scmi.viewscompra import compra
from scmi.viewsProveedor import proveedor
from scmi.viewsFacturacion import factura
from scmi.viewsCliente import cliente
from scmi.viewsInventerioMaterial import  material
from scmi.viewsPedido import  pedido
from scmi.viewsestadistica import  estadistica
from scmi.viewsDetallepedido import usomaterial
from scmi.viewarticulo import articulo
from scmi.viewsProforma import  proforma
from scmi.perfil import perfil
from scmi.viewstipomaterial import  tipomaterial
from scmi.viewsrecuperar import  recuperar
from scmi.viewsUsuario import  usuario
urlpatterns = [
    path('compra/' ,compra ,name='compra'),
    path('proveedor/' ,proveedor ,name='proveedor'),
    path('factura/' ,factura ,name='factura'),
    path('cliente/' ,cliente ,name='cliente'),
    path('material/' ,material ,name='material'),
    path('pedido/' ,pedido ,name='pedido'),
    path('estadistica/' ,estadistica ,name='estadistica'),
    path('detallepedido/' ,usomaterial ,name='usomaterial'),
    path('proforma/' ,proforma ,name='proforma'),
    path('articulo/' ,articulo ,name='articulo'),
    path('perfil/' ,perfil ,name='perfil'),
    path('tipomaterial/' ,tipomaterial ,name='tipomaterial'),
    path('recuperar/' ,recuperar ,name='recuperar'),
    path('usuario/' ,usuario ,name='usuario'),
]