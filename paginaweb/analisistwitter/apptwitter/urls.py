from django.conf.urls import include, url
from . import views

urlpatterns=[
	#ADMINISTRADOR
	url(r'^$',views.login,name='login'),
	url(r'^validarsesion$',views.validarsesion,name='validarsesion'),
    url(r'^analizar$',views.analizar,name='analizar'),
	url(r'^analisis$',views.analisis,name='analisis'),
	url(r'^index$',views.index,name='index'),
	url(r'^subirdocumento$',views.subirdocumento,name='subirdocumento'),
	url(r'^expedientes$',views.expedientes,name='expedientes'),
	url(r'^observar/(?P<idclave>\d+)/$',views.observar,name='observar'),
	url(r'^cerrar_sesion$',views.cerrar_sesion,name='cerrar_sesion'),
	url(r'^registrar$',views.registrar,name='registrar'),
]
