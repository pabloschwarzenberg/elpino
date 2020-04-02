# cursos/urls.py
from django.conf.urls import url,re_path
from django.urls import path,include,reverse
from covid19 import views

urlpatterns = [
    url(r'^$',views.HomePageView.as_view(),name="index"),
    url(r'noticias/', views.HomeNoticiasView.as_view(),name="noticias"),
    re_path(r'^noticia/(?P<pk>\d+)/$', views.DetalleNoticiaView.as_view(),name="detalle"),
    url(r'^noticia/create/$', views.NoticiaCreate.as_view(success_url='/noticias/'), name='noticia_create'),
    url(r'^noticia/(?P<pk>\d+)/update/$', views.NoticiaUpdate.as_view(success_url='/noticias/'), name='noticia_update'),
    url(r'^noticia/(?P<pk>\d+)/delete/$', views.NoticiaDelete.as_view(success_url='/noticias/'), name='noticia_delete'),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]