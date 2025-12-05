from django.db import models
from django.contrib.auth.models import User


class DataPoint(models.Model):
    label = models.CharField(max_length=100)
    value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.label}: {self.value}"
    

class Empresa(models.Model):
    propietario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=255)
    latitud = models.FloatField()
    longitud = models.FloatField()
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class SitioTuristico(models.Model):
    # 1. Identificación

    nit_sitio = models.CharField(max_length=50, blank=True, null=True)

    # 2. Información general
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)

    CATEGORIAS = [
        ('religioso', 'Religioso'),
        ('cultural', 'Cultural'),
        ('turistico', 'Turistico'),
        ('otro', 'Otro'),
    ]
    categoria = models.CharField(max_length=50, choices=CATEGORIAS, default='otro')

    etiquetas = models.CharField(max_length=255, blank=True, null=True)

    # 3. Ubicación
    pais = models.CharField(max_length=100)
    region = models.CharField(max_length=100, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    latitud = models.FloatField(blank=True, null=True)
    longitud = models.FloatField(blank=True, null=True)

    # 4. Información turística
    #horario_apertura = models.TimeField(blank=True, null=True)
    #horario_cierre = models.TimeField(blank=True, null=True)
    capaciad = models.CharField(blank=True, null=True)

    servicios_ofrecidos = models.CharField(max_length=1000,blank=True, null=True)

    # 6. Multimedia
    url_imagen_principal = models.URLField(max_length=255, blank=True, null=True)
    galeria_imagenes = models.TextField(blank=True, null=True)

    # 7. Administración y control
    ESTADOS_PUBLICACION = [
        ('borrador', 'Borrador'),
        ('publicado', 'Publicado'),
        ('archivado', 'Archivado'),
    ]
    estado_publicacion = models.CharField(max_length=20, choices=ESTADOS_PUBLICACION, default='borrador')

    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    registrado_por = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre
    

class Empresa(models.Model):
    propietario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=255)
    latitud = models.FloatField()
    longitud = models.FloatField()
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre