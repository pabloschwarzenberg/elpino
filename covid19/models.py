from django.db import models

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
