# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *
import pandas as pd
import json
from django.http import JsonResponse
from django.http import HttpResponse

from string import punctuation
import json_utils
from pandas.io.json import json_normalize
import pygsheets
import numpy as np
from django.utils.encoding import smart_unicode, smart_str
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def nubepalabras(df):
    listapalabras = []
    listatext=[]
    texto_nube=""
    jsone = df['entities_str'][:2000]
    for j in jsone:
        listapalabras.append(json.loads(j))
    for e in listapalabras:
        for ed in e['hashtags']:
            texto_nube = texto_nube + " "+ ed['text']
    #print(texto_nube)
    return texto_nube
def tweetsporfecha(df):
    listafechas=[]
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
    fecha = df.groupby(df["created_at"].dt.date).size().reset_index(name='count')
    for row in fecha.itertuples(index=True, name='Pandas'):
        listafechas.append({'fecha':str(getattr(row, "created_at")),'total':float(getattr(row, "count")),'color':'#FF6600'})
    #promedio = int(fecha['count'].mean())
    #print(listafechas)
    return listafechas
def usuarios_publicaciones(df):
    listausuarios=[]
    user = df.groupby(df["from_user"]).size().reset_index(name='count')
    usuarios = user.sort_values(by='count', ascending=False)[:10]
    for row in usuarios.itertuples(index=True, name='Pandas'):
        listausuarios.append({'usuario':str(getattr(row, "from_user")),'seguidores':float(getattr(row, "count"))})
    return listausuarios
#mapa
def ubicacion_tweets(df):
    listapais=[]
    listapais.append(['City','Tweets publicados'])
    numpaises = df.groupby(df["user_location"]).size().reset_index(name='count')
    paisesordenados = numpaises.sort_values(by='count', ascending=False)[:100]
    remplazado = paisesordenados.replace("",'xxxx')
    eliminados = remplazado[remplazado['user_location']!="xxxx"]
    paisesordenados = eliminados.sort_values(by='count', ascending=True)
    #print(paisesordenados)
    for row in paisesordenados.itertuples(index=True, name='Pandas'):
        listapais.append([smart_str(getattr(row, "user_location")),float(getattr(row, "count"))])
    return listapais

def lista_seguidores(df,valor):
    listaseguidores=[]
    listaseguidores.append(['Usuario','Numero de Seguidores'])
    numerostwitteros = df.groupby([df["from_user"],df['user_followers_count']]).size().reset_index(name='count')
    ordenadostwitteros = numerostwitteros.sort_values(by='user_followers_count', ascending=False)[:10]
    if valor == 1:
        try:
            remplazado = numerostwitteros.replace("",'xxxx')
            eliminados = remplazado[remplazado['user_followers_count']!="xxxx"]
            ordenadostwitteros = eliminados.sort_values(by='user_followers_count', ascending=False)[:10]
        except:
            pass
    for row in ordenadostwitteros.itertuples(index=True, name='Pandas'):
        #print(getattr(row, "user_followers_count"))
        listaseguidores.append([smart_str(getattr(row, "from_user")),getattr(row, "user_followers_count")])
    return listaseguidores
def galeria_fotos(df):
    listafotos = []
    listapalabras = []
    galeria=[]
    jsone = df['entities_str']
    for j in jsone:
        listapalabras.append(json.loads(j))

    lis = json.dumps(listapalabras)
    cargajson = json.loads(lis)
    for d in cargajson:
        try:
            listafotos.append(d['media'])
        except:
            print("pass")

    for l in listafotos:
        galeria.append(str(l[0]['media_url']))

    gal = pd.DataFrame(galeria)
    gal.columns = ['fotos']
    datos_fotos = gal.groupby(gal["fotos"]).size().reset_index(name='count')
    fotos_ordenadas = datos_fotos.sort_values(by='count', ascending=False)[:60]
    #print(fotos_ordenadas)
    galeria = []
    for row in fotos_ordenadas.itertuples(index=True, name='Pandas'):
        galeria.append({'url_foto':str(getattr(row, "fotos"))})
    return galeria
def tweet_porhora(df):
    listaporhora = []
    lista_tweets = []
    lista_retweets = []
    cont=0
    df['created_at_hora'] = pd.to_datetime(df.created_at)
    df['created_at_hora'] = df['created_at_hora'].dt.strftime('%H')
    df['text'] = df['text'].str[:2]
    dat_tweet = df.groupby([df["created_at_hora"],df['text']=='RT']).size().reset_index(name='count')
    retweets = dat_tweet[dat_tweet['text']==True]
    tweets = dat_tweet[dat_tweet['text']==False]
    tweets = tweets.groupby([tweets["created_at_hora"],tweets['count']]).size().reset_index(name='count3')
    retweets = retweets.groupby([retweets["created_at_hora"],retweets['count']]).size().reset_index(name='count3')
    dat_tweet = df.groupby(df["created_at_hora"]).size().reset_index(name='count')
    dat_tweet['countSNRT'] = tweets['count']
    dat_tweet['countRT'] = retweets['count']

    for row in dat_tweet.itertuples(index=True, name='Pandas'):
        listaporhora.append({'hora':str(getattr(row, "created_at_hora")),'reetweets':float(getattr(row, "countRT")),'tweets':float(getattr(row, "countSNRT"))})
        cont = cont + 1
    return listaporhora
def tweet_porDia(df):
    listaporDia = []
    df['created_at'] = pd.to_datetime(df.created_at)
    dia_semana = {0:'Lunes', 1:'Martes', 2:'Miercoles', 3:'Jueves', 4:'Viernes', 5:'Sabado', 6:'Domingo'}
    df['created_at'] = df['created_at'].dt.dayofweek.map(dia_semana)
    df['text'] = df['text'].str[:2]
    dat_tweet = df.groupby([df["created_at"],df['text']=='RT']).size().reset_index(name='count')
    retweets = dat_tweet[dat_tweet['text']==True]
    tweets = dat_tweet[dat_tweet['text']==False]
    tweets = tweets.groupby([tweets["created_at"],tweets['count']]).size().reset_index(name='count3')
    retweets = retweets.groupby([retweets["created_at"],retweets['count']]).size().reset_index(name='count3')
    dat_tweet = df.groupby(df["created_at"]).size().reset_index(name='count')
    dat_tweet['countSNRT'] = tweets['count']
    dat_tweet['countRT'] = retweets['count']
    sorter = ['Domingo', 'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado']
    sorterIndex = dict(zip(sorter,range(len(sorter))))
    dat_tweet['dia_id'] = dat_tweet['created_at']
    dat_tweet['dia_id'] = dat_tweet['dia_id'].map(sorterIndex)
    ordenados = dat_tweet.sort_values(by='dia_id', ascending=True)
    for row in ordenados.itertuples(index=True, name='Pandas'):
        listaporDia.append({'dia':str(getattr(row, "created_at")),'reetweets':float(getattr(row, "countRT")),'tweets':float(getattr(row, "countSNRT"))})
    return listaporDia

def analizar(request):
    listaresultados = []
    lista_datotweet = []
    valor=0
    if request.method == 'POST':
        if 'analizargoogle' in request.POST:
            keydocumento = request.POST['urlarchivo']
            existe_documento = DocumentosGoogle.objects.filter(archivo_key = keydocumento).exists()
            nombre_analisis = request.POST['nombre_analisis']
            nombre_archivo = request.POST['nombre_archivo']
            gc = pygsheets.authorize(outh_file='drivetwitter-687ecebee5ac.json')
            gc = pygsheets.authorize()
            sht1 = gc.open_by_key(str(keydocumento))
            wks = sht1.worksheet('index', 1)
            df = wks.get_as_df()
            lista_datotweet = []
            valor = 1
            if existe_documento is True:
                doc_google = DocumentosGoogle.objects.get(archivo_key = keydocumento)
            else:
                doc_google = DocumentosGoogle()
                doc_google.usuario = request.user
                doc_google.archivo_key = keydocumento
                doc_google.nombre_archivo = nombre_archivo
                doc_google.save()

            direccion_documento = "archivosgoogle/"+nombre_analisis+".xlsx"
            writer = df.to_excel(direccion_documento, index=False)
            analisis_anterior = AnalisisAnteriores()
            analisis_anterior.documentogoogle = doc_google
            analisis_anterior.direccion_documento = direccion_documento
            analisis_anterior.nombre_analisis = nombre_analisis
            analisis_anterior.save()
        if 'analizarexcel' in request.POST:
            keydocumento = request.FILES['Fichier1']
            nombreanalisis = request.POST['nombreanalisis']
            tweet_excel = DocumentosExcel()
            tweet_excel.usuario = request.user
            tweet_excel.archivo = keydocumento
            tweet_excel.nombre_analisis = nombreanalisis
            tweet_excel.save()

            df = pd.read_excel("/home/edisonchavezsa/Escritorio/Repositorios/python/Analisis_twitter/paginaweb/analisistwitter/"+str(tweet_excel.archivo))

        promedio=""
        fechaanalizado = ""
        request.session['error'] = tweetsporfecha(df)
        request.session['usuarios'] = usuarios_publicaciones(df)
        request.session['promedio'] = promedio
        request.session['paises'] = ubicacion_tweets(df)
        request.session['listaseguidores'] = lista_seguidores(df,valor)
        request.session['texto'] = nubepalabras(df)
        request.session['datTweet'] = lista_datotweet
        request.session['listaporhora'] = tweet_porhora(df)
        request.session['galeriafoto'] = galeria_fotos(df)
        request.session['listaporDia'] = tweet_porDia(df)

        request.session['fechaanalizado'] = fechaanalizado

    return HttpResponseRedirect(reverse('analisis'))

def login(request):

    ctx={'hola':'hola'}
    return render(request, 'login.html',ctx)

def analisis(request):
    lista_enviar = []
    lista_usuarios = []
    listapaises = []
    listaseguidores = []
    datTweet = []
    listaporhora=[]
    galeriafoto = []
    listaporDia = []
    texto = ""
    fechaanalizado = ""
    promedio = 0
    if request.session.has_key('error'):
        lista_enviar = request.session.get('error')
        lista_usuarios = request.session.get('usuarios')
        promedio = request.session.get('promedio')
        listapaises = request.session.get('paises')
        listaseguidores = request.session.get('listaseguidores')
        datTweet = request.session.get('datTweet')
        listaporhora = request.session.get('listaporhora')
        texto = request.session.get('texto')
        galeriafoto = request.session.get('galeriafoto')
        listaporDia = request.session.get('listaporDia')

        del request.session['error']

    ctx={'hola':'hola','lista':json.dumps(lista_enviar),'listausuarios':json.dumps(lista_usuarios),
    'promedio':promedio,'listapaises':json.dumps(listapaises),'listaseguidores':json.dumps(listaseguidores),'texto':texto,'datTweet':datTweet,
    'listaporhora':json.dumps(listaporhora),'fechaanalizado':fechaanalizado,'galeriafoto':galeriafoto,'listaporDia':json.dumps(listaporDia)}
    return render(request, 'analisis.html',ctx)

def subirdocumento(request):
    ctx={'hola':'hola'}
    return render(request, 'subirdocumento.html',ctx)


def index(request):
    lista_documentos = []
    numdocumentos = DocumentosGoogle.objects.filter(usuario = request.user.pk).count()
    if numdocumentos > 0:
        documentos = DocumentosGoogle.objects.filter(usuario = request.user.pk)[:4]
        for d in documentos:
            lista_documentos.append({'keydocumento':d.archivo_key,'nombre_archivo':d.nombre_archivo,'fechaingreso':str(d.fechaingreso.date())})
    ctx={'documentonumero':numdocumentos,'lista_documentos':lista_documentos}
    return render(request, 'carga_documento.html',ctx)

def expedientes(request):
    lista_documentos = []
    cont = 1
    analisis_anterior = AnalisisAnteriores.objects.filter(documentogoogle__usuario = request.user).order_by("-fecha_analisis")
    for a in analisis_anterior:
        lista_documentos.append({'id':cont,'nombredocumento':a.documentogoogle.nombre_archivo,
        'nombre_analisis':a.nombre_analisis,'fecha_analisis':str(a.fecha_analisis.date()),'idclave':a.pk})
        cont = cont + 1
    ctx={'expedientes':lista_documentos}
    return render(request, 'expedientes.html',ctx)

def observar(request,idclave):
    lista_documentos = []
    analisis = AnalisisAnteriores.objects.get(id_analisisanteriores = idclave)
    keydocumento = analisis.direccion_documento
    df = pd.read_excel(keydocumento)
    lista_datotweet=[]
    valor=0
    promedio=""
    fechaanalizado = ""
    request.session['error'] = tweetsporfecha(df)
    request.session['usuarios'] = usuarios_publicaciones(df)
    request.session['promedio'] = promedio
    request.session['paises'] = ubicacion_tweets(df)
    request.session['listaseguidores'] = lista_seguidores(df,valor)
    request.session['texto'] = nubepalabras(df)
    request.session['datTweet'] = lista_datotweet
    request.session['listaporhora'] = tweet_porhora(df)
    request.session['galeriafoto'] = galeria_fotos(df)
    request.session['listaporDia'] = tweet_porDia(df)

    request.session['fechaanalizado'] = fechaanalizado

    return HttpResponseRedirect(reverse('analisis'))

def cerrar_sesion(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

def registrar(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        correo = request.POST['correo']
        usuario = request.POST['usuario']
        password = request.POST['password']
        existe_usuario = User.objects.filter(username=usuario).exists()
        if existe_usuario is False:
            existe_correo = User.objects.filter(email=correo).exists()
            if existe_correo is False:
                user = User.objects.create_user(username=usuario,first_name=nombre,last_name=apellido,email=correo,password=password)
        else:
            print("ya existe el usuario")
    return HttpResponseRedirect(reverse('login'))

def validarsesion(request):
    username = request.POST['usuario']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    ctx={'latest_question_list': 'latest_question_list'}
    print(user)
    if user is not None:
        auth_login(request, user)
        if user.is_active == True:
            return HttpResponseRedirect(reverse('index'))
    else:
        pass
    return HttpResponseRedirect(reverse('login'))
