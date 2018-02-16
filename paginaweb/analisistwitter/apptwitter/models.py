# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
# Create your models here.

class Tweetsanalizado(models.Model):
    id_analisis = models.AutoField(primary_key=True)
    fechaingreso = models.TimeField(default=datetime.now())
    archvio = models.FileField(blank=True, upload_to='archivosgoogle')
    analizado = models.NullBooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'tweetsanalizado'

class DocumentosGoogle(models.Model):
    id_documentogoogle = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    fechaingreso = models.DateTimeField(default = datetime.now())
    nombre_archivo = models.CharField(max_length=450,null=True)
    archivo_key = models.CharField(max_length=450)

class DocumentosExcel(models.Model):
    id_documentoexcel = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    fechaingreso = models.DateTimeField(default = datetime.now())
    archivo = models.FileField(blank=True, upload_to='archivos')
    nombre_analisis = models.CharField(max_length=450)

class AnalisisAnteriores(models.Model):
    id_analisisanteriores = models.AutoField(primary_key=True)
    documentogoogle = models.ForeignKey(DocumentosGoogle, on_delete=models.CASCADE,null=True)
    fecha_analisis = models.DateTimeField(default = datetime.now())
    direccion_documento = models.CharField(max_length=550)
    nombre_analisis = models.CharField(max_length=450,null=True)
