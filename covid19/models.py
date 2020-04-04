from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
import os

# Create your models here.
class Noticia(models.Model):
    fecha=models.DateTimeField()
    titulo=models.CharField(max_length=128)
    imagen=models.CharField(max_length=256)
    descripcion=models.CharField(max_length=1024)
    noticias=models.Manager()

    def __str__(self):
        return "{}".format(self.titulo)

class Documento(models.Model):
    ARCHIVO = 0
    ALGORITMO = 1
    VIDEO = 2
    TIPO_CHOICES = [
        (ARCHIVO, 'Archivo'),
        (ALGORITMO, 'Algoritmo'),
        (VIDEO, 'Video'),
    ]
    tipo = models.IntegerField(
        choices=TIPO_CHOICES,
        default=ARCHIVO,
    )
    titulo=models.CharField(max_length=128)
    link=models.CharField(max_length=256,blank=True,null=True)
    archivo=models.FileField(blank=True,null=True,upload_to='documents/%Y/%m/%d/')
    documentos=models.Manager()

    def delete(self, *args, **kwargs):
        if(self.archivo):
            os.remove(os.path.join(settings.MEDIA_ROOT, self.archivo.name))
        super(Documento,self).delete(*args,**kwargs)

class Estadistica(models.Model):
    fecha=models.DateField()
    casos_Chile=models.FloatField()
    hospital_T1=models.FloatField()
    hospital_T2=models.FloatField()
    hospital_T3=models.FloatField()
    hospital_T4=models.FloatField()
    hospital_contagios=models.FloatField()
    hospital_lm=models.FloatField()
    estadisticas=models.Manager()

SERVICIOS = (
        (1, 'Servicio 1'),
        (2, 'Servicio 2'),
)

ACTIVIDADES = (
        (1, 'Clínico'),
        (2, 'Administrativo'),
)

class Usuario(AbstractUser):
    nombre = models.CharField(max_length=30)
    apellido_paterno = models.CharField(max_length=30)
    apellido_materno = models.CharField(max_length=30)
    fecha_nacimiento = models.DateField()
    funcionario = models.BooleanField()
    servicio = models.IntegerField(choices=SERVICIOS,blank=True,null=True)
    actividad = models.IntegerField(choices=ACTIVIDADES,blank=True,null=True)
    email = models.EmailField(max_length=254, help_text='')

class Contacto(models.Model):
    usuario=models.ForeignKey(Usuario,on_delete=models.CASCADE)
    fecha_registro=models.DateTimeField(auto_now_add=True)
    contacto_confirmado=models.BooleanField()
    sintomas=models.BooleanField()
    contacto_10minutos=models.BooleanField()
    contacto_2horas=models.BooleanField()
    contactos=models.Manager()
    status=models.IntegerField()


