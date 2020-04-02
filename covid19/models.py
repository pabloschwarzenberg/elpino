from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

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
    link=models.CharField(max_length=256)
    archivo=models.FileField(blank=True,null=True,upload_to='documents/%Y/%m/%d/')
    documentos=models.Manager()

class Estadistica(models.Model):
    casos_Q1=models.FloatField()
    casos_Q2=models.FloatField()
    casos_Q3=models.FloatField()
    casos_Q4=models.FloatField()
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
    contacto_confirmado=models.BooleanField()
    sintomas=models.BooleanField()
    contacto_10minutos=models.BooleanField()
    contacto_2horas=models.BooleanField()
    contactos=models.Manager()



