from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
class TipoMaterial(models.Model):
    nombre=models.CharField(max_length=100,blank=True,default=" ")
    status=models.BooleanField(default=True)
    def __str__(self):
        return '{}'.format(self.nombre)
    class Meta:
        verbose_name = 'Tipo Material'
        verbose_name_plural = 'Tipo Materiales'
        ordering = ['nombre']

class Material(models.Model):
    material = models.CharField(max_length=200,default=" ")
    tipo = models.ForeignKey(TipoMaterial, blank=True, null=True, on_delete=models.PROTECT)
    arprecio = models.DecimalField(decimal_places=0, max_digits=19,default=0)
    stock= models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    def __str__(self):
        return '{}'.format(self.material)
    class Meta:
        verbose_name = 'Materialll'
        verbose_name_plural = 'Materialll'
        ordering = ['material']

TIPOINVENTARIO = (
    (1,'Compra'),
    (2,'Ingreso'),
    (3,'Modificado'),
    (4,'Produccion'),)

class Inventario(models.Model):
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    fechaingreso =models.DateTimeField(default=datetime.now(), blank=True)
    fechasalida =models.DateTimeField(default=None, blank=True,null=True)
    cantidad = models.IntegerField(default=0)
    precio = models.DecimalField(decimal_places=0,max_digits=19, default=0)
    tipoinventario = models.IntegerField(choices=TIPOINVENTARIO, default=2)
    status = models.BooleanField(default=True)
    class Meta:
        verbose_name = 'Inventario General'
        verbose_name_plural = 'Inventario General'
        ordering = ['material']

TIPOClien_Provee = (
    (1,'Cliente'),
    (2,'Proveedor'))
class CliProentidad(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="EMPRESA",default='')
    tipo = models.IntegerField(choices=TIPOClien_Provee, default=0)
    direccion = models.CharField(max_length=200,verbose_name="DIRECCION",default='')
    telefono = models.CharField(max_length=200,verbose_name="TELEFONO",default='')
    ced_ruc = models.CharField(max_length=200, verbose_name="Cedula o Ruc",default='')
    status = models.BooleanField(default=True)
    email=models.CharField(max_length=200,default="")
    def __str__(self):
        return '{}'.format(self.nombre)

    class Meta:
        verbose_name = 'Cliente o Proveedor'
        verbose_name_plural = 'Cliente o Proveedor'
        ordering = ['nombre']

class Empresa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre =models.CharField(max_length=60,verbose_name="nombre",default='')
    cedula=  models.CharField(max_length=15,verbose_name="cedula",default='')
    direcion=  models.CharField(max_length=50,verbose_name="direccion",default='')
    celular =models.CharField(max_length=50,verbose_name="celular",default='')
    image = models.ImageField(upload_to='empresa/%Y/%m/%d/', default='')
    def __str__(self):
        return '{}'.format(self.cedula)
    class Meta:
        verbose_name = 'Empresa dato'
        verbose_name_plural = 'Empresa dato'
        ordering = ['cedula']

class Compra(models.Model):
    fecha = models.DateTimeField(default=datetime.now(), blank=True)
    total = models.DecimalField(decimal_places=0, max_digits=19,default=0)
    cliProentidad = models.ForeignKey(CliProentidad,on_delete=models.PROTECT)
    status = models.BooleanField(default=True)
    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        ordering = ['id']

class Comprainventario(models.Model):
    salidacompra = models.ForeignKey(Compra,on_delete=models.PROTECT)
    cantidad = models.IntegerField(default=0)
    valor = models.DecimalField(decimal_places=0, max_digits=19,default=0)
    material = models.ForeignKey(Material, on_delete=models.PROTECT,default=None)
    status = models.BooleanField(default=True)
    class Meta:

        verbose_name = 'Detalle de Compra'
        verbose_name_plural = 'Detalle de Compra'
        ordering = ['id']

class Articulo(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="articulo",default='')
    descripcion = models.CharField(max_length=200, verbose_name="descripción",default='')
    cantidad = models.IntegerField(verbose_name="cantidad",default=0)
    iva = models.DecimalField(decimal_places=2, verbose_name="iva",max_digits=19,default=0.12)
    subtotal = models.DecimalField(decimal_places=0, verbose_name="subtotal",max_digits=19,default=0)
    precio = models.DecimalField(decimal_places=0, verbose_name="Precio",max_digits=19,default=0)
    image = models.ImageField(upload_to='Articulo/%Y/%m/%d/', default='')
    status = models.BooleanField(default=True)
    def __str__(self):
        return '{}'.format(self.nombre)
    class Meta:
        verbose_name = 'Articulo'
        verbose_name_plural = 'Articulos'
        ordering = ['nombre']

class Pedido(models.Model):
    descripcion = models.CharField(max_length=150,default='')
    fecentrega = models.DateTimeField(default=datetime.now())
    coutainicial = models.DecimalField(decimal_places=0, verbose_name="coutainicial",max_digits=19,default=0)
    cliProentidad = models.ForeignKey(CliProentidad, on_delete=models.PROTECT,default=None)
    status = models.BooleanField(default=True)
    abono = models.DecimalField(decimal_places=0, verbose_name="coutainicial", max_digits=19, default=0)
    class Meta:
        verbose_name = 'Pedido de Clientes Articulo'
        verbose_name_plural = 'Pedido de Clientes articulos'
        ordering = ['fecentrega']

class Pedidoarticulo(models.Model):
    articulo = models.ForeignKey(Articulo, on_delete=models.PROTECT,default=None)
    cantidad = models.IntegerField(verbose_name="cantidad", default=0)
    abono = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT,default=None)
    class Meta:
        verbose_name = 'Pedido de detalle Articulo'
        verbose_name_plural = 'Pedido de detalle articulos'
        ordering = ['articulo']

class Pedidodetalle (models.Model):
    cantidad = models.IntegerField(verbose_name="cantidad",default=0)
    material = models.ForeignKey(Material, on_delete=models.PROTECT,default=None)
    descripcion = models.CharField(max_length=150, default='')
    status = models.BooleanField(default=True)
    class Meta:
        verbose_name = 'Materiales que se usaran en el Pedido'
        verbose_name_plural = 'Materiales que se usaran en el Pedido'
        ordering = ['id']
class Factura(models.Model):
    cliente = models.ForeignKey(CliProentidad, on_delete=models.PROTECT)
    fecventa = models.DateTimeField(default=datetime.now())
    iva = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    total = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    status = models.BooleanField(default=True)
    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Factura'
        ordering = ['id']
class Proforma(models.Model):
    empresa = models.ForeignKey(Empresa,on_delete=models.PROTECT)
    fec = models.DateTimeField(default=datetime.now())
    total = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    status = models.BooleanField(default=True)
    descripcion = models.CharField(max_length=150, default='')
    class Meta:
        verbose_name = 'Proforma'
        verbose_name_plural = 'Proforma'
        ordering = ['id']
class DetalleProforma(models.Model):
    proforma = models.ForeignKey(Proforma, on_delete=models.PROTECT)
    articulo = models.ForeignKey(Articulo, on_delete=models.PROTECT)
    descripcion = models.CharField(max_length=150,default='')
    cantidad = models.IntegerField(verbose_name="cantidad",default=0)
    total = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    status = models.BooleanField(default=True)
    maximo = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    class Meta:
        verbose_name = 'DetalleProforma'
        verbose_name_plural = 'DetalleProforma'
        ordering = ['id']
class Detfactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.PROTECT)
    articulo = models.ForeignKey(Articulo, on_delete=models.PROTECT)
    cantidad = models.IntegerField(verbose_name="cantidad",default=0)
    total = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    status = models.BooleanField(default=True)
    class Meta:
        verbose_name = 'Detalle factura'
        verbose_name_plural = 'Detalle factura'
        ordering = ['id']
class Reporteventa(models.Model):
    mes =models.IntegerField(verbose_name='mes',default=0)
    año = models.IntegerField(default=0,verbose_name='año')
    total = models.DecimalField(default=0, max_digits=10, decimal_places=2,verbose_name='total')
    def __str__(self):
        return '{}-{}-{}'.format(self.mes,self.año,self.total)
    class Meta:
        verbose_name ='Reporte'
        verbose_name_plural ='reportes'
        ordering =['id']


def month_string_to_number(string):
    m = { "Ener": 1,"Febr": 2,"Marz": 3,"Abri":4,"Mayo":5,"Juni":6,"Juli":7,"Agos":8,"Sept":9,"Octu":10,"Novi":11,"Dici":12}
    s = string.strip()[:4].capitalize()
    try:
        out = m[s]
        return out,True
    except:
        return 0, False