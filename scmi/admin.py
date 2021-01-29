from django.contrib import admin

from scmi.models import  Pedidoarticulo, TipoMaterial,Material,Inventario,CliProentidad,Compra,Comprainventario,Articulo,Detfactura,Factura,Pedido,Pedidodetalle,Empresa,Proforma,DetalleProforma,Reporteventa


admin.site.register(TipoMaterial)
admin.site.register(Reporteventa)

admin.site.register(Inventario)
admin.site.register(Pedidoarticulo)

admin.site.register(CliProentidad)

admin.site.register(Compra)


admin.site.register(Material)

admin.site.register(Comprainventario)

admin.site.register(Articulo)


admin.site.register(Detfactura)

admin.site.register(Factura)




admin.site.register(Pedido)

admin.site.register(Pedidodetalle)



admin.site.register(Empresa)
admin.site.register(Proforma)

admin.site.register(DetalleProforma)