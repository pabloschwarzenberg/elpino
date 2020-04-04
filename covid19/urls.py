# cursos/urls.py
from django.conf.urls import url,re_path
from django.urls import path,include,reverse
from covid19 import views

urlpatterns = [
    url(r'^$',views.HomePageView.as_view(),name="index"),
    url(r'noticias/', views.HomeNoticiasView.as_view(),name="noticias"),
    url(r'estadisticas/', views.HomeEstadisticasView.as_view(),name="estadisticas"),
    url(r'^estadistica/create/$', views.EstadisticaCreate.as_view(success_url='/estadisticas/'), name='estadistica_create'),
    url(r'contacto/', views.ContactoCreate.as_view(),name="contacto"),
    re_path(r'^evaluacion/(?P<pk>\d+)/$', views.ContactoEvaluationView.as_view(),name="contacto_evaluacion"),
    url(r'algoritmos/', views.HomeAlgoritmosView.as_view(),name="algoritmos"),
    url(r'biblioteca/', views.HomeBibliotecaView.as_view(),name="biblioteca"),
    url(r'^documento/create/$', views.DocumentoCreate.as_view(success_url='/biblioteca/'), name='documento_create'),
    url(r'^documento/(?P<pk>\d+)/update/$', views.DocumentoUpdate.as_view(success_url='/biblioteca/'), name='documento_update'),
    url(r'^documento/(?P<pk>\d+)/delete/$', views.DocumentoDelete.as_view(success_url='/biblioteca/'), name='documento_delete'),
    re_path(r'^documento/(?P<pk>\d+)/$', views.DetalleDocumentoView.as_view(),name="detalleDocumento"),
    url(r'videos/', views.HomeVideosView.as_view(),name="videos"),
    re_path(r'^noticia/(?P<pk>\d+)/$', views.DetalleNoticiaView.as_view(),name="detalle"),
    url(r'^noticia/create/$', views.NoticiaCreate.as_view(success_url='/noticias/'), name='noticia_create'),
    url(r'^noticia/(?P<pk>\d+)/update/$', views.NoticiaUpdate.as_view(success_url='/noticias/'), name='noticia_update'),
    url(r'^noticia/(?P<pk>\d+)/delete/$', views.NoticiaDelete.as_view(success_url='/noticias/'), name='noticia_delete'),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('contagios_chart/', views.contagios_chart, name='contagios_chart'),
]