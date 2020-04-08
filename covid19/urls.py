# cursos/urls.py
from django.conf.urls import url,re_path
from django.urls import path,include,reverse
from covid19 import views

urlpatterns = [
    url(r'^$',views.HomePageView.as_view(),name="index"),
    url(r'noticias/', views.HomeNoticiasView.as_view(),name="noticias"),
    url(r'estadisticas/', views.HomeEstadisticasView.as_view(),name="estadisticas"),
    url(r'^estadistica/list/$', views.HomeEstadisticasListView.as_view(),name="estadistica_list"),
    url(r'^estadistica/create/$', views.EstadisticaCreate.as_view(success_url='/estadisticas/'), name='estadistica_create'),
    url(r'^estadistica/(?P<pk>\d+)/update/$', views.EstadisticaUpdate.as_view(success_url='/estadistica/list/'), name='estadistica_update'),
    url(r'^estadistica/(?P<pk>\d+)/delete/$', views.EstadisticaDelete.as_view(success_url='/estadistica/list/'), name='estadistica_delete'),
    url(r'contacto/', views.ContactoCreate.as_view(),name="contacto"),
    re_path(r'^evaluacion/(?P<pk>\d+)/$', views.ContactoEvaluationView.as_view(),name="contacto_evaluacion"),
    url(r'biblioteca/', views.HomeBibliotecaView.as_view(),name="biblioteca"),
    url(r'algoritmos/', views.HomeAlgoritmosView.as_view(),name="algoritmos"),
    url(r'videos/', views.HomeVideosView.as_view(),name="videos"),
    url(r'^documento/create/(?P<tipo>0)/$', views.DownloadDocumentCreate.as_view(success_url='/biblioteca/'), name='documento_create0'),
    url(r'^documento/create/(?P<tipo>1)/$', views.DownloadDocumentCreate.as_view(success_url='/algoritmos/'), name='documento_create1'),
    url(r'^documento/create/(?P<tipo>2)/$', views.VideoCreate.as_view(success_url='/videos/'), name='documento_create2'),
    url(r'^documento/(?P<pk>\d+)/update/(?P<tipo>0)/$', views.DownloadDocumentUpdate.as_view(success_url='/biblioteca/'), name='documento_update0'),
    url(r'^documento/(?P<pk>\d+)/update/(?P<tipo>1)/$', views.DownloadDocumentUpdate.as_view(success_url='/algoritmos/'), name='documento_update1'),
    url(r'^documento/(?P<pk>\d+)/update/(?P<tipo>2)/$', views.VideoUpdate.as_view(success_url='/videos/'), name='documento_update2'),
    url(r'^documento/(?P<pk>\d+)/delete/(?P<tipo>0)/$', views.DocumentoDelete.as_view(success_url='/biblioteca/'), name='documento_delete0'),
    url(r'^documento/(?P<pk>\d+)/delete/(?P<tipo>1)/$', views.DocumentoDelete.as_view(success_url='/algoritmos/'), name='documento_delete1'),
    url(r'^documento/(?P<pk>\d+)/delete/(?P<tipo>2)/$', views.DocumentoDelete.as_view(success_url='/videos/'), name='documento_delete2'),
    re_path(r'^documento/(?P<pk>\d+)/$', views.DetalleDocumentoView.as_view(),name="detalleDocumento"),
    re_path(r'^noticia/(?P<pk>\d+)/$', views.DetalleNoticiaView.as_view(),name="detalle"),
    url(r'^noticia/create/$', views.NoticiaCreate.as_view(success_url='/noticias/'), name='noticia_create'),
    url(r'^noticia/(?P<pk>\d+)/update/$', views.NoticiaUpdate.as_view(success_url='/noticias/'), name='noticia_update'),
    url(r'^noticia/(?P<pk>\d+)/delete/$', views.NoticiaDelete.as_view(success_url='/noticias/'), name='noticia_delete'),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('casos_chile_chart/', views.casos_chile_chart, name='casos_chile_chart'),
    path('casos_hospital_chart/', views.casos_hospital_chart, name='casos_hospital_chart'),
    url(r'about/', views.AboutView.as_view(),name="about"),
]