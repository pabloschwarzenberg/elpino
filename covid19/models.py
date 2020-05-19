from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
import os

# Create your models here.
class Noticia(models.Model):
    fecha=models.DateTimeField()
    titulo=models.CharField(max_length=128)
    autor=models.CharField(max_length=128)
    imagen=models.FileField(upload_to='news/%Y/%m/%d/')
    descripcion=models.CharField(max_length=1024)
    noticias=models.Manager()

    def __str__(self):
        return "{}".format(self.titulo)

    def delete(self, *args, **kwargs):
        if(self.imagen):
            os.remove(os.path.join(settings.MEDIA_ROOT, self.imagen.name))
        super(Noticia,self).delete(*args,**kwargs)

class Documento(models.Model):
    ARCHIVO = 0
    ALGORITMO = 1
    VIDEO = 2
    TIPO_CHOICES = [
        (ARCHIVO, 'Archivo'),
        (ALGORITMO, 'Flujograma'),
        (VIDEO, 'Video'),
    ]
    tipo = models.IntegerField(
        choices=TIPO_CHOICES,
        default=ARCHIVO,
    )
    titulo=models.CharField(max_length=128)
    link=models.CharField(max_length=256,blank=True,null=True)
    archivo=models.FileField(blank=True,null=True,upload_to='documents/%Y/%m/%d/')
    fecha=models.DateTimeField(auto_now_add=True)
    documentos=models.Manager()

    def delete(self, *args, **kwargs):
        if(self.archivo):
            os.remove(os.path.join(settings.MEDIA_ROOT, self.archivo.name))
        super(Documento,self).delete(*args,**kwargs)

class Estadistica(models.Model):
    fecha=models.DateField()
    confirmados_Hospital=models.IntegerField()
    examenes_Hospital=models.IntegerField()
    hospital_VMI=models.IntegerField()
    hospital_TOTAL=models.IntegerField()
    funcionarios_contagiados=models.IntegerField()
    funcionarios_PCR=models.IntegerField()
    estadisticas=models.Manager()

SERVICIOS = (
        (1, 'Servicio 1'),
        (2, 'Servicio 2'),
)

ACTIVIDADES = (
        (1, 'Médico'),
        (2, 'Profesional de la Salud'),
        (3, 'Técnico de la Salud'),
        (4, 'Administrativo'),
)

TIPO_CONTRATO = (
        (1, 'Contrata'),
        (2, 'Honorario'),
        (3, 'Otro')
)

class Usuario(AbstractUser):
    nombre = models.CharField(max_length=30)
    apellido_paterno = models.CharField(max_length=30)
    apellido_materno = models.CharField(max_length=30)
    fecha_nacimiento = models.DateField()
    servicio = models.CharField(max_length=30)
    actividad = models.IntegerField(choices=ACTIVIDADES,default=1)
    contrato=models.IntegerField(choices=TIPO_CONTRATO,default=3)
    email = models.EmailField(max_length=254, help_text='')
    telefono = models.CharField(max_length=30)

class Contacto(models.Model):
    usuario=models.ForeignKey(Usuario,on_delete=models.CASCADE)
    fecha_registro=models.DateTimeField(auto_now_add=True)
    contacto_confirmado=models.BooleanField()
    sintomas=models.BooleanField()
    contacto_10minutos=models.BooleanField()
    contacto_2horas=models.BooleanField()
    contactos=models.Manager()
    status=models.IntegerField()


