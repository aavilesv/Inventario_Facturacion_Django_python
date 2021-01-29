from django.db import models
from django.contrib.auth.models import User, Group
class Modulo(models.Model):
    url = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    icono = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)

    def __str__(self):
        return '{}'.format(self.nombre)

    class Meta:
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'
        ordering = ['orden']


class ModuloGrupo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200, blank=True)
    modulos = models.ManyToManyField(Modulo)
    grupos = models.ManyToManyField(Group)
    prioridad = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.nombre)

    class Meta:
        verbose_name = 'Grupo de Módulos'
        verbose_name_plural = 'Grupos de Módulos'
        ordering = ('prioridad', 'nombre')

    def modulos_activos(self):
        return self.modulos.filter(activo=True).order_by('orden')
